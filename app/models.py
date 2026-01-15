from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class Sport(str, Enum):
    SWIM = "swim"
    BIKE = "bike"
    RUN = "run"


class RaceDistance(str, Enum):
    SPRINT = "sprint"  # 750m swim, 20km bike, 5km run
    OLYMPIC = "olympic"  # 1.5km swim, 40km bike, 10km run
    HALF_IRONMAN = "half_ironman"  # 1.9km swim, 90km bike, 21.1km run
    FULL_IRONMAN = "full_ironman"  # 3.8km swim, 180km bike, 42.2km run


class FitnessLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class WorkoutInterval(BaseModel):
    duration_minutes: Optional[int] = None
    distance_km: Optional[float] = None
    intensity: str  # e.g., "Zone 2", "Easy", "Threshold", "Recovery"
    description: str


class Workout(BaseModel):
    sport: Sport
    title: str
    total_duration_minutes: int
    total_distance_km: Optional[float] = None
    warmup: str
    main_set: List[WorkoutInterval]
    cooldown: str
    notes: Optional[str] = None


class WeekPlan(BaseModel):
    week_number: int
    focus: str  # e.g., "Base Building", "Threshold Work", "Race Week"
    workouts: List[Workout]
    weekly_volume_hours: float
    weekly_distance_km: float


class TrainingProgram(BaseModel):
    goal: RaceDistance
    fitness_level: FitnessLevel
    duration_weeks: int
    weeks: List[WeekPlan]
    notes: str


class WorkoutRequest(BaseModel):
    goal: RaceDistance
    fitness_level: FitnessLevel
    available_hours_per_week: int = Field(ge=3, le=30)
    current_week: int = Field(default=1, ge=1)
    duration_weeks: int = Field(default=12, ge=4, le=52)
    focus_areas: Optional[List[str]] = None  # e.g., ["swimming technique", "bike endurance"]
