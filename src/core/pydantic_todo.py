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

    def __eq__(self, o):
        if not isinstance(o, Todo):
            raise TypeError

        if self.id != o.id:
            return False
        if self.user_id != o.user_id:
            return False
        if self.description != o.description:
            return False
        if self.date_created != o.date_created:
            return False
        if self.date_due != o.date_due:
            return False
        if self.priority != o.priority:
            return False
        if self.completed != o.completed:
            return False

        return True
