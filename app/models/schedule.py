from sqlmodel import Field, SQLModel
from typing import Optional

class Schedule(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key = "user.id")
    exercise_name: str
    day_of_week: str
    sets: Optional[int] = None
    reps: Optional[int] = None
    muscle: Optional[str] = None