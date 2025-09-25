from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from src.common import PriorityType

class Todo(BaseModel):
    id: Optional[int] # optional since when creating we won't have an id
    user_id: int
    description: str
    date_created: datetime
    date_due: Optional[datetime]
    priority: PriorityType
    completed: bool
