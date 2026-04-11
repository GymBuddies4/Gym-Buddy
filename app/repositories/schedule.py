from sqlmodel import Session, select
from app.models.schedule import Schedule
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class ScheduleRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, schedule: Schedule) -> Schedule:
        try:
            self.db.add(schedule)
            self.db.commit()
            self.db.refresh(schedule)
            return schedule
        except Exception as e:
            logger.error(f"An error occured while saving schedule: {e}")
            self.db.rollback()
            raise

    def get_by_user(self, user_id: int) -> list[Schedule]:
        return self.db.exec(select(Schedule).where(Schedule.user_id == user_id)).all()

    def get_by_user_and_day(self, user_id: int, day_of_week: str) -> list[Schedule]:
        return self.db.exec(
            select(Schedule).where(
                Schedule.user_id == user_id,
                Schedule.day_of_week == day_of_week
            )
        ).all()
    
    def delete(self, schedule_id: int, user_id: int):
        schedule = self.db.exec(
            select(Schedule).where(
                Schedule.id == schedule_id,
                Schedule.user_id == user_id
            )
        ).one_or_none()
        if not schedule:
            raise Exception("Schedule item not found")
        try:
            self.db.delete(schedule)
            self.db.commit()
        except Exception as e:
            logger.error(f"An error occurred while deleting schedule: {e}")
            self.db.rollback()
            raise