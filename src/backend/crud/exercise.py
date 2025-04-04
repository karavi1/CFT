from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from src.backend.models.exercise import Exercise
from src.backend.schemas.exercise import ExerciseCreate, ExerciseUpdate

def create_exercise(db: Session, exercise_data: ExerciseCreate):
    exercise = Exercise(**exercise_data.model_dump())
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise

def create_batch_exercise(db: Session, exercises_data: List[ExerciseCreate]):
    exercises_list = []
    for exercise_data in exercises_data:
        exercise = Exercise(**exercise_data.model_dump())
        db.add(exercise)
        db.commit()
        db.refresh(exercise)
        exercises_list += [exercise]
    return exercises_list

def get_exercise_by_id(db: Session, exercise_id: UUID):
    return db.query(Exercise).filter(Exercise.id == exercise_id).first()

def get_all_exercises(db: Session):
    return db.query(Exercise).all()

def update_exercise(db: Session, exercise_id: UUID, updates: ExerciseUpdate):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        return None
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(exercise, field, value)
    db.commit()
    db.refresh(exercise)
    return exercise

def delete_exercise(db: Session, exercise_id: UUID):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        return False
    db.delete(exercise)
    db.commit()
    return True