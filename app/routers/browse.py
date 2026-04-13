from fastapi import APIRouter, Request, Query
from typing import Optional
from app.routers import templates
from app.services.exercise_service import search_exercises

router = APIRouter()

@router.get("/browse")
def browse_page(
    request: Request,
    muscle: Optional[str] = Query(default=None),
    type: Optional[str] = Query(default=None),
):
    exercises = search_exercises(muscle=muscle, exercise_type=type)

    return templates.TemplateResponse(
        request=request,
        name="browse.html",
        context={
            "request": request,
            "exercises": exercises,
            "muscle": muscle,
            "type": type,
        },
    )