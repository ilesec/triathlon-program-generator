from typing import Dict, Any
from anthropic import Anthropic
import json
from app.config import settings
from app.models import (
    WorkoutRequest,
    TrainingProgram,
    RaceDistance,
    FitnessLevel,
)


class TriathlonWorkoutAgent:
    """AI Agent for generating structured triathlon training programs."""
    
    def __init__(self):
        self.client = Anthropic(api_key=settings.anthropic_api_key)
        self.model = "claude-3-5-sonnet-20241022"
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt for the workout generation agent."""
        return """You are an expert triathlon coach with 20+ years of experience training athletes for Sprint, Olympic, Half Ironman, and Full Ironman distances.

Your role is to create structured, periodized training programs that include:
- Swim, bike, and run workouts
- Specific intervals with duration/distance and intensity zones
- Proper warmup and cooldown protocols
- Progressive overload and recovery weeks
- Monthly periodization (base, build, peak, taper phases)

Key principles:
1. **Intensity Zones**: Use these standard zones:
   - Zone 1: Recovery (very easy, conversational)
   - Zone 2: Aerobic/Endurance (comfortable, still conversational)
   - Zone 3: Tempo (moderately hard, some breathing effort)
   - Zone 4: Threshold (hard, sustained effort)
   - Zone 5: VO2 Max (very hard, short intervals)

2. **Periodization**: Structure programs in phases:
   - Base Phase (60-70% of total time): Build aerobic base, Zone 2 focus
   - Build Phase (20-30%): Add intensity, Zone 3-4 work
   - Peak Phase (5-10%): Race-specific intensity
   - Taper Phase (1-2 weeks): Reduce volume, maintain intensity

3. **Weekly Structure**: Balance stress and recovery:
   - Hard days followed by easy/recovery days
   - Long endurance sessions on weekends
   - Brick workouts (bike-to-run transitions)
   - At least 1 full rest day per week

4. **Progression**: Increase volume by 10-15% per week max, with recovery weeks every 3-4 weeks.

You must respond with valid JSON matching the TrainingProgram schema."""

    def _build_user_prompt(self, request: WorkoutRequest) -> str:
        """Build the user prompt with specific workout requirements."""
        
        race_distances = {
            RaceDistance.SPRINT: "Sprint (750m swim, 20km bike, 5km run)",
            RaceDistance.OLYMPIC: "Olympic (1.5km swim, 40km bike, 10km run)",
            RaceDistance.HALF_IRONMAN: "Half Ironman (1.9km swim, 90km bike, 21.1km run)",
            RaceDistance.FULL_IRONMAN: "Full Ironman (3.8km swim, 180km bike, 42.2km run)",
        }
        
        prompt = f"""Create a {request.duration_weeks}-week training program for the following athlete:

**Goal**: {race_distances[request.goal]}
**Fitness Level**: {request.fitness_level.value}
**Available Training Time**: {request.available_hours_per_week} hours per week
**Current Week**: Week {request.current_week}
"""
        
        if request.focus_areas:
            prompt += f"**Focus Areas**: {', '.join(request.focus_areas)}\n"
        
        prompt += """
Generate a complete training program with the following structure:

**Required JSON Format**:
```json
{
  "goal": "race_distance",
  "fitness_level": "level",
  "duration_weeks": number,
  "weeks": [
    {
      "week_number": 1,
      "focus": "Base Building",
      "workouts": [
        {
          "sport": "swim|bike|run",
          "title": "Workout Title",
          "total_duration_minutes": 60,
          "total_distance_km": 5.0,
          "warmup": "10 min easy swim, drills",
          "main_set": [
            {
              "duration_minutes": 20,
              "distance_km": 2.0,
              "intensity": "Zone 2",
              "description": "Continuous aerobic swim"
            }
          ],
          "cooldown": "5 min easy",
          "notes": "Focus on technique"
        }
      ],
      "weekly_volume_hours": 6.5,
      "weekly_distance_km": 50.0
    }
  ],
  "notes": "Program overview and key focus areas"
}
```

**Guidelines**:
1. Create 5-7 workouts per week based on available hours
2. Include all three sports (swim, bike, run) appropriately distributed
3. Each workout must have specific intervals with intensity zones
4. Include at least one brick workout per week (bike followed by run)
5. Progressively increase volume with recovery weeks every 3-4 weeks
6. Return ONLY the JSON, no additional text or markdown formatting
"""
        
        return prompt
    
    def generate_program(self, request: WorkoutRequest) -> TrainingProgram:
        """Generate a complete training program using Claude."""
        
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(request)
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=8000,
            temperature=0.7,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )
        
        # Extract the JSON from the response
        content = response.content[0].text
        
        # Remove markdown code blocks if present
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        # Parse JSON and validate with Pydantic
        program_data = json.loads(content)
        program = TrainingProgram(**program_data)
        
        return program
    
    def generate_single_week(
        self, 
        request: WorkoutRequest,
        week_number: int,
        phase: str
    ) -> Dict[str, Any]:
        """Generate a single week of training (useful for ongoing programs)."""
        
        prompt = f"""Create Week {week_number} of a {request.duration_weeks}-week {request.goal.value} training program.

**Phase**: {phase}
**Fitness Level**: {request.fitness_level.value}
**Available Hours**: {request.available_hours_per_week} hours

Return a JSON object for this single week following the WeekPlan schema.
"""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            temperature=0.7,
            system=self._build_system_prompt(),
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        content = response.content[0].text
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        
        return json.loads(content)
