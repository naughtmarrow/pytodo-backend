from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from src.common import PriorityType

class Todo(BaseModel):
    id: int
    user_id: int
    description: str
    date_created: datetime
    date_due: Optional[datetime]
    priority: PriorityType
    completed: bool
