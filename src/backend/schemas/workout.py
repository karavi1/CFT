from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date
from typing import Optional, List
from src.backend.schemas.logged_exercise import LoggedExerciseCreateByName, LoggedExerciseOut  

class WorkoutBase(BaseModel):
    workout_date: Optional[date] = None
    notes: Optional[str] = None

class WorkoutCreate(WorkoutBase):
    user_id: UUID
    logged_exercises: List[LoggedExerciseOut] = Field(..., min_length=1)

class WorkoutCreateSimple(BaseModel):
    username: str
    notes: Optional[str] = None
    logged_exercises: List[LoggedExerciseCreateByName] = Field(..., min_length=1)

class WorkoutUpdate(WorkoutBase):
    notes: Optional[str]

class WorkoutOut(WorkoutBase):
    id: UUID
    user_id: UUID
    workout_date: date
    logged_exercises: List[LoggedExerciseOut] = []

    model_config = {
        "from_attributes": True
    }