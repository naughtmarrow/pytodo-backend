from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: Optional[int] # optional since when creating we won't have an id
    name: str
    password: str
