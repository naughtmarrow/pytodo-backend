from typing import List

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.core import Todo

from . import TransactionManager
from .SAClasses import _SATodo, _SAUser


#  WARN: EXPERIMENTAL BUILD WITH A MIXED CREATE/UPDATE QUERY
def save_todo(td: Todo, tm: TransactionManager) -> Todo:
    try:
        sat = _SATodo(
            user_id=td.user_id,
            description=td.description,
            date_created=td.date_created,
            date_due=td.date_due,
            priority=td.priority,
            completed=td.completed,
        )

        if td.user_id is not None:
            sat.id=td.id

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
            completed=sat.completed,
        )

        return ntd

    except Exception as e:
        # TODO: Add logging here and consider using specific files and named exceptions
        # for different layers
        raise e


def get_todo_id(todo_id: int, tm: TransactionManager) -> Todo:
    try:
        td: _SATodo = (
            tm._session.execute(select(_SATodo).where(_SATodo.id == todo_id))
            .scalars()
            .one()
        )

        return Todo(
            id=td.id,
            user_id=td.user_id,
            description=td.description,
            date_created=td.date_created,
            date_due=td.date_due,
            priority=td.priority,
            completed=td.completed,
        )

    except Exception as e:
        # TODO: Add logging here and consider using specific files and named exceptions
        # for different layers
        raise e


def get_todos_from_user(user_id: int, tm: TransactionManager) -> List[Todo]:
    try:
        result_person: _SAUser = (
            tm._session.execute(
                select(_SAUser)
                .where(_SAUser.id == user_id)
                .options(selectinload(_SAUser.things))
            )
            .scalars()
            .all()
        )

        tdlist: List[Todo] = []
        for td in result_person.things:
            tdlist.append(
                Todo(
                    id=td.id,
                    user_id=td.user_id,
                    description=td.description,
                    date_created=td.date_created,
                    date_due=td.date_due,
                    priority=td.priority,
                    completed=td.completed,
                )
            )

        return tdlist
    except Exception as e:
        # TODO: Add logging here and consider using specific files and named exceptions
        # for different layers
        raise e

def delete_todo(todo: Todo, tm: TransactionManager) -> bool:  # type: ignore
    try:
        tm._session.delete(todo)
        tm._session().flush()
        return True
    except Exception as e:
        # TODO: Add logging here and consider using specific files and named exceptions
        # for different layers
        raise e
