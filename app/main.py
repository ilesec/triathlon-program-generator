from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import json
import uvicorn

from app.database import init_db, get_db
from app.models import WorkoutRequest, TrainingProgram, RaceDistance, Sport
from app.agent import TriathlonWorkoutAgent
from app.repository import ProgramRepository, WorkoutHistoryRepository

# Initialize FastAPI app
app = FastAPI(
    title="Triathlon Program Generator",
    description="AI-powered triathlon training program generator",
    version="1.0.0"
)

# Initialize database
init_db()

# Setup templates
templates = Jinja2Templates(directory="app/templates")

# Initialize agent
agent = TriathlonWorkoutAgent()


# API Endpoints

@app.post("/api/workouts/generate", response_model=dict)
async def generate_workout(
    request: WorkoutRequest,
    db: Session = Depends(get_db)
):
    """Generate a new training program using the AI agent."""
    try:
        # Generate program using AI
        program = agent.generate_program(request)
        
        # Save to database
        saved_program = ProgramRepository.save_program(
            db=db,
            program=program,
            request_data=request.model_dump()
        )
        
        return {
            "id": saved_program.id,
            "program": program.model_dump(),
            "message": "Training program generated successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating program: {str(e)}")


@app.get("/api/workouts", response_model=List[dict])
async def list_workouts(
    skip: int = 0,
    limit: int = 100,
    goal: Optional[RaceDistance] = None,
    db: Session = Depends(get_db)
):
    """List all saved workout programs."""
    programs = ProgramRepository.list_programs(
        db=db,
        skip=skip,
        limit=limit,
        goal=goal.value if goal else None
    )
    
    return [
        {
            "id": p.id,
            "created_at": p.created_at.isoformat(),
            "goal": p.goal,
            "fitness_level": p.fitness_level,
            "duration_weeks": p.duration_weeks,
            "available_hours_per_week": p.available_hours_per_week,
            "notes": p.notes
        }
        for p in programs
    ]


@app.get("/api/workouts/{program_id}", response_model=dict)
async def get_workout(program_id: int, db: Session = Depends(get_db)):
    """Get a specific workout program by ID."""
    program = ProgramRepository.get_program(db=db, program_id=program_id)
    
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    
    return {
        "id": program.id,
        "created_at": program.created_at.isoformat(),
        "goal": program.goal,
        "fitness_level": program.fitness_level,
        "duration_weeks": program.duration_weeks,
        "program": json.loads(program.program_json)
    }


@app.delete("/api/workouts/{program_id}")
async def delete_workout(program_id: int, db: Session = Depends(get_db)):
    """Delete a workout program."""
    success = ProgramRepository.delete_program(db=db, program_id=program_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Program not found")
    
    return {"message": "Program deleted successfully"}


@app.post("/api/history/log")
async def log_workout(
    program_id: Optional[int] = None,
    sport: Sport = Sport.RUN,
    title: str = "Workout",
    duration_minutes: int = 60,
    distance_km: Optional[float] = None,
    notes: Optional[str] = None,
    rating: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Log a completed workout."""
    workout = WorkoutHistoryRepository.log_workout(
        db=db,
        program_id=program_id,
        sport=sport.value,
        title=title,
        duration_minutes=duration_minutes,
        distance_km=distance_km,
        notes=notes,
        rating=rating
    )
    
    return {
        "id": workout.id,
        "message": "Workout logged successfully"
    }


@app.get("/api/history")
async def get_workout_history(
    program_id: Optional[int] = None,
    sport: Optional[Sport] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get workout history."""
    workouts = WorkoutHistoryRepository.get_workout_history(
        db=db,
        program_id=program_id,
        sport=sport.value if sport else None,
        skip=skip,
        limit=limit
    )
    
    return [
        {
            "id": w.id,
            "completed_at": w.completed_at.isoformat(),
            "sport": w.sport,
            "title": w.title,
            "duration_minutes": w.duration_minutes,
            "distance_km": w.distance_km,
            "notes": w.notes,
            "rating": w.rating
        }
        for w in workouts
    ]


@app.get("/api/stats")
async def get_stats(sport: Optional[Sport] = None, db: Session = Depends(get_db)):
    """Get workout statistics."""
    stats = WorkoutHistoryRepository.get_workout_stats(
        db=db,
        sport=sport.value if sport else None
    )
    return stats


# Web Interface

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main web interface."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/programs/{program_id}", response_class=HTMLResponse)
async def view_program(request: Request, program_id: int):
    """View a specific training program."""
    return templates.TemplateResponse(
        "program.html",
        {"request": request, "program_id": program_id}
    )


if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 8000))
    print(f"Starting Triathlon Program Generator on port {port}...")
    print(f"Navigate to http://localhost:{port} to access the web interface")
    uvicorn.run(app, host="0.0.0.0", port=port)
