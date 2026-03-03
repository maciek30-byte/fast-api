from pydantic import BaseModel, Field
from typing import Optional

class TodoRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3)
    description: str = Field(min_length=3)
    is_completed: bool
    priority: Optional[int] = None