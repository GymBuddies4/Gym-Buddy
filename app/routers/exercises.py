from typing import List
from fastapi import APIRouter, Query

from app.schemas.exercise import ExerciseResponse
from app.services.exercise_service import fetch_exercises

router = APIRouter(prefix="/exercises", tags=["Exercises"])


@router.get("/", response_model=List[ExerciseResponse])
def get_exercises(muscle: str = Query(..., description="Muscle group to search")):
    return fetch_exercises(muscle)