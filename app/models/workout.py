from sqlmodel import Field, SQLModel
from typing import Optional

class WorkoutCategories(SQLModel):
    name: str = Field(index = True)
    category: str = Field(index = True)
    sets: int
    reps: str
    description: str = ""

class Workout(WorkoutCategories, table = True):
    id: Optional[int] = Field(default = None, primary_key = True)
