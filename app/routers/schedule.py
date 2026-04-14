from fastapi import Request, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from app.dependencies import SessionDep
from app.dependencies.auth import AuthDep
from app.repositories.schedule import ScheduleRepository
from app.services.exercise_service import search_exercises
from app.models.schedule import Schedule
from . import router, templates

@router.get("/my-workout", response_class=HTMLResponse)
async def my_workout_view(request: Request, user: AuthDep, db: SessionDep):
    repo = ScheduleRepository(db)
    all_schedules = repo.get_by_user(user.id)

    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    schedule = [
        {
            "name": day,
            "workouts": [s for s in all_schedules if s.day_of_week.lower() == day.lower()]

        }
        for day in days
    ]

    return templates.TemplateResponse(
        request=request,
        name="my_workout.html",
        context = {"user": user, "schedule": schedule}
    )

@router.get("/my-workout/{schedule_id}", response_class=HTMLResponse)
async def workout_detail_view(
    request: Request,
    schedule_id: int,
    user: AuthDep,
    db: SessionDep,
):
    repo = ScheduleRepository(db)
    workout = repo.get_one_by_user(schedule_id, user.id)

    if not workout:
        return RedirectResponse(
            url=request.url_for("my_workout_view"),
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        request=request,
        name="workout_detail.html",
        context={
            "request": request,
            "user": user,
            "workout": workout,
        }
    )    

@router.post("/my-workout/add", response_class=HTMLResponse)
async def add_to_schedule(
    request: Request,
    user: AuthDep,
    db: SessionDep,
    exercise_name: str = Form(),
    day_of_week: str = Form(),
    muscle: str = Form(default=None),
    sets: int = Form(default=None),
    reps: str = Form(default=None),
):
    repo = ScheduleRepository(db)
    schedule = Schedule(
        user_id = user.id,
        exercise_name = exercise_name,
        day_of_week = day_of_week,
        muscle = muscle,
        sets = sets,
        reps = reps,
    )
    repo.create(schedule)
    return RedirectResponse(url=request.url_for("my_workout_view"), status_code=status.HTTP_303_SEE_OTHER)

@router.post("/delete-workout/{schedule_id}")
async def delete_from_schedule(
    request: Request,
    schedule_id: int,
    user: AuthDep,
    db: SessionDep,
):
    
    repo = ScheduleRepository(db)
    try:
        repo.delete(schedule_id, user.id)
    except Exception:
        pass
    return RedirectResponse(url=request.url_for("my_workout_view"), status_code=status.HTTP_303_SEE_OTHER)

@router.get("/my-workout/list")
async def get_my_workout_list(user: AuthDep, db: SessionDep):
    repo = ScheduleRepository(db)
    schedules = repo.get_by_user(user.id)
    return [s.exercise_name.lower() for s in schedules]