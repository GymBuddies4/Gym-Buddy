from typing import Optional
from pydantic import BaseModel


class ExerciseResponse(BaseModel):
    name: str
    type: Optional[str] = None
    muscle: Optional[str] = None
    equipment: Optional[str] = None
    difficulty: Optional[str] = None
    instructions: Optional[str] = None