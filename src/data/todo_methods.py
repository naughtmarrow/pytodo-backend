from typing import List

from src.core import Todo

from . import TransactionManager
from .SAClasses import _SATodo


def save_todo(td: Todo, tm: TransactionManager) -> Todo:
    try:
        sat = _SATodo(
            user_id=td.user_id,
            description=td.description,
            date_created=td.date_created,
            date_due=td.date_due,
            priority=td.priority,
            completed=td.completed
        )

        tm._session().add(sat)
        tm._session().flush()
        tm._session().refresh(sat)

        ntd: Todo = Todo(
            id=sat.id,
            user_id=sat.user_id,
            description=sat.description,
            date_created=sat.date_created,
            date_due=sat.date_due,
            priority=sat.priority,
            completed=sat.completed
        )

        return ntd

    except Exception as e:
        # TODO: Add logging here and consider using specific files and named exceptions
        # for different layers
        raise e


def get_todo_id(todo_id: int, tm: TransactionManager) -> Todo:  # type: ignore
    pass


def get_todos_from_user(user_id: int, tm: TransactionManager) -> List[Todo]:  # type: ignore
    pass


def update_todo(td: Todo, tm: TransactionManager) -> bool:
    try:
        sat = _SATodo(
            user_id=td.user_id,
            description=td.description,
            date_created=td.date_created,
            date_due=td.date_due,
            priority=td.priority,
            completed=td.completed
        )

        tm._session().add(sat)
        tm._session().flush()

        return True

    except Exception as e:
        # TODO: Add logging here and consider using specific files and named exceptions
        # for different layers
        raise e


def delete_todo(todo_id: int, tm: TransactionManager) -> bool:  # type: ignore
    return True
