from pydantic import BaseModel
from typing import Optional

# WARN: honestly probably shouldn't have the password of the user just hanging around
# in the backend if we can avoid it
class User(BaseModel):
    id: Optional[int] # optional since when creating we won't have an id
    username: str
    password: str
