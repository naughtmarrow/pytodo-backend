from typing import List

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.core import Todo

from . import TransactionManager
from .SAClasses import _SATodo, _SAUser


#  WARN: EXPERIMENTAL BUILD WITH A MIXED CREATE/UPDATE QUERY
def save_todo(td: Todo, tm: TransactionManager) -> Todo:
    """
    Saves changes made to a todo object in database and creates a new todo if one does not exist.
    Parameters:
        - td: An object of type Todo to be saved
        - tm: An instance of TransactionManager to manage the session
    Returns:
        An object of type todo with the information that was saved to the database
    
    Usage:
        new_todo = save_todo(td, tm)
    """
    try:
        sat = _SATodo(
            user_id=td.user_id,
            description=td.description,
            date_created=td.date_created,
            date_due=td.date_due,
            priority=td.priority,
            completed=td.completed,
        )

        tm.add(sat)
        tm.flush()
        tm.refresh(sat)

        return Todo(
            id=sat.id,
            user_id=sat.user_id,
            description=sat.description,
            date_created=sat.date_created,
            date_due=sat.date_due,
            priority=sat.priority,
            completed=sat.completed,
        )

    except Exception as e:
        # TODO: Add logging here and consider using specific files and named exceptions
        # for different layers
        raise e


def get_todo_id(todo_id: int, tm: TransactionManager) -> Todo:
    try:
        td: _SATodo = (
            tm.execute(select(_SATodo).where(_SATodo.id == todo_id))
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
            tm.execute(
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
        tm.delete(todo)
        tm.flush()
        return True
    except Exception as e:
        # TODO: Add logging here and consider using specific files and named exceptions
        # for different layers
        raise e
