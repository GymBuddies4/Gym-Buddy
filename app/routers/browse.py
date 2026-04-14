from fastapi import APIRouter, Request, Query
from typing import Optional
from app.routers import templates
from app.services.exercise_service import search_exercises
from app.dependencies import SessionDep
from app.dependencies.auth import AuthDep
from app.repositories.schedule import ScheduleRepository

router = APIRouter()


def filter_exercises(exercises, query: Optional[str]):
    if not query:
        return exercises

    query = query.lower()
    return [
        ex for ex in exercises
        if query in ex["name"].lower()
    ]


@router.get("/browse")
def browse_page(
    request: Request,
    user: AuthDep,
    db: SessionDep,
    muscle: Optional[str] = Query(default=None),
    type: Optional[str] = Query(default=None),
    q: Optional[str] = Query(default=None),
):
    
    if muscle or type:
        exercises = search_exercises(muscle=muscle, exercise_type=type)
    else:
        muscles = [
            "chest", "back", "biceps", "triceps",
            "quadriceps", "hamstrings", "abdominals",
        ]
        exercises = []
        for m in muscles:
            try:
                exercises += search_exercises(muscle=m)
            except:
                pass
        seen = set()
        unique_exercises = []
        for ex in exercises:
            name = ex["name"]
            if name not in seen:
                seen.add(name)
                unique_exercises.append(ex)
        exercises = unique_exercises

    exercises = filter_exercises(exercises, q)

    # Get names of exercises the user already added
    repo = ScheduleRepository(db)
    user_schedules = repo.get_by_user(user.id)
    added_exercise_names = {s.exercise_name.lower() for s in user_schedules}

    return templates.TemplateResponse(
        request=request,
        name="browse.html",
        context={
            "request": request,
            "exercises": exercises,
            "muscle": muscle,
            "type": type,
            "q": q,
            "added_exercise_names": added_exercise_names,
        },
    )