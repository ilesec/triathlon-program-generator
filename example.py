"""
Example script demonstrating how to use the Triathlon Program Generator programmatically.
"""

from app.agent import TriathlonWorkoutAgent
from app.models import WorkoutRequest, RaceDistance, FitnessLevel
import json


def main():
    # Initialize the agent
    print("Initializing Triathlon Program Generator...")
    agent = TriathlonWorkoutAgent()
    
    # Create a workout request
    request = WorkoutRequest(
        goal=RaceDistance.OLYMPIC,
        fitness_level=FitnessLevel.INTERMEDIATE,
        available_hours_per_week=10,
        duration_weeks=12,
        focus_areas=["swimming technique", "bike endurance"]
    )
    
    print("\nGenerating training program...")
    print(f"Goal: {request.goal.value}")
    print(f"Fitness Level: {request.fitness_level.value}")
    print(f"Available Hours: {request.available_hours_per_week}/week")
    print(f"Duration: {request.duration_weeks} weeks")
    
    # Generate the program
    program = agent.generate_program(request)
    
    # Display results
    print("\n" + "="*80)
    print("TRAINING PROGRAM GENERATED")
    print("="*80)
    
    print(f"\nProgram Overview:")
    print(f"Goal: {program.goal.value.upper()}")
    print(f"Total Weeks: {program.duration_weeks}")
    print(f"\n{program.notes}")
    
    # Display first week in detail
    if program.weeks:
        week1 = program.weeks[0]
        print(f"\n" + "-"*80)
        print(f"WEEK 1 - {week1.focus}")
        print("-"*80)
        print(f"Weekly Volume: {week1.weekly_volume_hours} hours")
        print(f"Weekly Distance: {week1.weekly_distance_km} km")
        print(f"\nWorkouts:")
        
        for i, workout in enumerate(week1.workouts, 1):
            print(f"\n{i}. {workout.title} ({workout.sport.value.upper()})")
            print(f"   Duration: {workout.total_duration_minutes} minutes")
            if workout.total_distance_km:
                print(f"   Distance: {workout.total_distance_km} km")
            print(f"   Warmup: {workout.warmup}")
            print(f"   Main Set:")
            for interval in workout.main_set:
                duration_str = f"{interval.duration_minutes}min" if interval.duration_minutes else ""
                distance_str = f"{interval.distance_km}km" if interval.distance_km else ""
                print(f"      - {duration_str} {distance_str} @ {interval.intensity}")
                print(f"        {interval.description}")
            print(f"   Cooldown: {workout.cooldown}")
    
    # Save to JSON file
    output_file = "example_program.json"
    with open(output_file, 'w') as f:
        json.dump(program.model_dump(), f, indent=2)
    
    print(f"\n\nFull program saved to: {output_file}")
    print("\n✅ Example completed successfully!")


if __name__ == "__main__":
    main()
