from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from src.backend.schemas.logged_exercise import LoggedExerciseCreateByName, LoggedExerciseOut  
from src.backend.models.enums import ExerciseGroup

class WorkoutBase(BaseModel):
    notes: Optional[str] = None
    workout_type: Optional[ExerciseGroup] = None

class WorkoutCreate(WorkoutBase):
    user_id: UUID
    logged_exercises: List[LoggedExerciseOut] = Field(..., min_length=1)

class WorkoutCreateSimple(BaseModel):
    username: str
    created_time: Optional[datetime] = None
    notes: Optional[str] = None
    workout_type: Optional[ExerciseGroup] = None
    logged_exercises: List[LoggedExerciseCreateByName] = Field(..., min_length=1)

class WorkoutUpdate(BaseModel):
    notes: Optional[str] = None
    created_time: Optional[datetime] = None
    workout_type: Optional[ExerciseGroup] = None
    logged_exercises: Optional[List[LoggedExerciseCreateByName]] = None

    model_config = {
        "use_enum_values": True
    }

class WorkoutOut(WorkoutBase):
    id: UUID
    user_id: UUID
    created_time: datetime
    logged_exercises: List[LoggedExerciseOut] = []

    model_config = {
        "from_attributes": True
    }