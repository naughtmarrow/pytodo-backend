from src.core import User
from src.data.SAClasses import _SAUser

from . import TransactionManager
from sqlalchemy import select


def save_user(usr: User, tm: TransactionManager) -> User:
    try:
        sau = _SAUser(
            username=usr.username,
            password=usr.password,  # WARN: probably should change this later
        )

        tm.add(sau)
        tm.flush()
        tm.refresh(sau)

        return User(id=sau.id, username=sau.username, password=sau.password)

    except Exception as e:
        # TODO: Add logging here and consider using specific files and named exceptions
        # for different layers
        raise e


def get_user_id(user_id: int, tm: TransactionManager) -> User:  # type: ignore
    try:
        sau: _SAUser = (
            tm.execute(select(_SAUser).where(_SAUser.id == user_id))
            .scalars()
            .one()
        )

        return User(id=sau.id, username=sau.username, password=sau.password)

    except Exception as e:
        # TODO: Add logging here and consider using specific files and named exceptions
        # for different layers
        raise e
    pass


def delete_user(user: User, tm: TransactionManager) -> bool:  # type: ignore
    try:
        tm.delete(user)
        tm.flush()
        return True
    except Exception as e:
        # TODO: Add logging here and consider using specific files and named exceptions
        # for different layers
        raise e
    return True
