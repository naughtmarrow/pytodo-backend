from typing import Optional

from pydantic import BaseModel


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

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return True # for now we don't have anonymous users i guess

    def is_active(self):
        return True # for now we won't have user deactivation systems

    def is_anonymous(self) -> bool:
        return False # for now we don't have anonymous users
