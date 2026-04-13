from fastapi import APIRouter, Request, Query
from typing import Optional
from app.routers import templates
from app.services.exercise_service import search_exercises

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
    muscle: Optional[str] = Query(default=None),
    type: Optional[str] = Query(default=None),
    q: Optional[str] = Query(default=None),
):
    
    if muscle or type:
        print(f"Total exercises found: {len(exercises)}")
        print(f"First few exercises: {exercises[:3] if exercises else 'None'}")
        exercises = search_exercises(muscle=muscle, exercise_type=type)

    else:
        muscles = [
            "chest",
            "back",
            "biceps",
            "triceps",
            "quadriceps",
            "hamstrings",
            "abdominals",
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

    if not q:  
        all_names = [ex["name"] for ex in exercises]
        print(f"Available exercises: {sorted(set(all_names))[:20]}")

    return templates.TemplateResponse(
        request=request,
        name="browse.html",
        context={
            "request": request,
            "exercises": exercises,
            "muscle": muscle,
            "type": type,
            "q": q,
        },
    )