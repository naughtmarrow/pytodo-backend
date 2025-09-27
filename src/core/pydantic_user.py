from pydantic import BaseModel
from typing import Optional

# WARN: honestly probably shouldn't have the password of the user just hanging around
# in the backend if we can avoid it
class User(BaseModel):
    id: Optional[int] # optional since when creating we won't have an id
    username: str
    password: Optional[str] # optional since we don't want to take this all over the place
    # password will probably only ever be loaded into this object during signup to simplify the insertion mechanism

    def __eq__(self, o):
        if isinstance(o, User):
            raise TypeError

        if self.id != o.id:
            return False
        if self.username != o.username:
            return False
        if self.password != o.password:
            return False
