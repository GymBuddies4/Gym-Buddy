from sqlmodel import Session, select, func
from app.models.workout import WorkoutCategories, Workout
from typing import Optional, Tuple
from app.utilities.pagination import Pagination
import logging

logger = logging.getLogger(__name__)

class WorkoutRepository:
    def __init__(self, db: Session):
        self.db = db

def create(self, workout_data: WorkoutCategories) -> Optional[Workout]:
    try:
        workout_db = Workout.model_validate(workout_data)
        self.db.add(workout_db)
        self.db.commit()
        self.db.refresh(workout_db)
        return workout_db
    except Exception as e:
        logger.error(f"An error has occurred: {e}")
        self.db.rollback()
        raise

def get_by_id(self, workout_id: int) -> Optional[Workout]:
    return self.db.get(Workout, workout_id)

def get_all(self) -> list[Workout]:
    return self.db.exec(select(Workout)).all()

def get_by_category(self, category:str) -> list[Workout]:
    return self.db.exec(select(Workout).where(Workout.category == category)).all()

def search_workouts(self, query: str, page: int = 1, limit: int = 10) -> Tuple[list[Workout], Pagination]:
    offset = (page - 1) * limit
    db_qry = select(Workout)
    if query:
        db_qry = db_qry.where(
            Workout.name.ilike(f"%{query}%") | Workout.category.ilike(f"%{query}%")
        )
    count_qry = select(func.count()).select_from(db_qry.subquery())
    count_workouts = self.db.exec(count_qry).one()

    workouts = self.db.exec(db_qry.offset(offset).limit(limit)).all()
    pagination = Pagination(total_count=count_workouts, current_page = page, limit = limit)

    return workouts, pagination

def delete_workout(self, workout_id: int):
    workout = self.db.get(Workout, workout_id)
    if not workout:
        raise Exception("Workout does not exist")
    try:
        self.db.delete(workout)
        self.db.commit()
    except Exception as e:
        logger.error(f"An error occurred while deleting workout: {e}")
        self.db.rollback()
        raise