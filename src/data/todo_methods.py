from typing import List

from sqlalchemy import Connection, text

from src.core import Todo
from src.common import PriorityType


def save_todo(td: Todo, conn: Connection) -> int:
    """
    Saves changes made to a todo object in database and creates a new todo if one does not exist.
    Parameters:
        - td: An object of type Todo to be saved
        - conn: A connection to execute queries from
    Returns:
        The primary key (id) of the inserted todo object in the database.

    Usage:
        new_id = save_todo(td, tm)
    """
    try:
        query = text(
            "INSERT INTO todos (user_id, description, date_created, date_due, priority, completed)"
            + "VALUES (:user_id, :description, :date_created, :date_due, :priority, :completed) RETURNING id"
        )

        id = (
            conn.execute(
                query,
                {
                    "user_id": td.user_id,
                    "description": td.description,
                    "date_created": td.date_created,
                    "date_due": td.date_due,
                    "priority": td.priority,
                    "completed": td.completed,
                },
            )
            .one()
            .id
        )

        return id
    except Exception as e:
        # TODO: Add logging here and consider using specific files and named exceptions
        # for different layers
        raise e


def get_todo_id(todo_id: int, conn: Connection) -> Todo:
    """
    Returns a todo object with the requested id from the database.
    Parameters:
        - todo_id: An integer corresponding to the id value of a todo object in the database
        - conn: A connection to execute queries from
    Returns:
        A todo object with the data corresponding to that of the todo item in the database.

    Usage:
        todo = get_todo_id(todo_id, conn)
    """
    try:
        query = text("SELECT * FROM todos WHERE id = :id")
        td = conn.execute(query, {"id": todo_id}).fetchone()._mapping  # type: ignore

        return Todo(
            id=td.id,
            user_id=td.user_id,
            description=td.description,
            date_created=td.date_created,
            date_due=td.date_due,
            priority=PriorityType[td.priority],
            completed=td.completed,
        )
    except Exception as e:
        # TODO: Add logging here and consider using specific files and named exceptions
        # for different layers
        raise e


def get_todos_from_user(user_id: int, conn: Connection) -> List[Todo]:
    """
    Returns a list of todo objects related to the given user id from the database.
    Parameters:
        - user_id: An integer corresponding to the id value of a user object in the database.
        - conn: A connection to execute queries from
    Returns:
        A list of todo objects with the data corresponding to that of the todo items in the database related to the given user.

    Usage:
        todo = get_todo_id(todo_id, conn)
    """
    try:
        query = text("SELECT * FROM todos WHERE user_id = :user_id")
        rows = conn.execute(query, {"user_id": user_id}).fetchall()

        tdlist: List[Todo] = []
        for td in rows:
            tdlist.append(
                Todo(
                    id=td.id,
                    user_id=td.user_id,
                    description=td.description,
                    date_created=td.date_created,
                    date_due=td.date_due,
                    priority=PriorityType[td.priority],
                    completed=td.completed,
                )
            )

        return tdlist
    except Exception as e:
        # TODO: Add logging here and consider using specific files and named exceptions
        # for different layers
        raise e


def update_todo(td: Todo, conn: Connection) -> Todo:
    try:
        query = text(
            "UPDATE todos SET user_id = :user_id, description = :description,"
            + "date_created = :date_created, date_due =  :date_due,"
            + "priority = :priority, completed = :completed"
            + "WHERE id = :id RETURNING *"
        )

        res = conn.execute(
            query,
            {
                "id": td.id,
                "user_id": td.user_id,
                "description": td.description,
                "date_created": td.date_created,
                "date_due": td.date_due,
                "priority": td.priority,
                "completed": td.completed,
            },
        ).one()._mapping

        return Todo(**res)
    except Exception as e:
        # TODO: Add logging here and consider using specific files and named exceptions
        # for different layers
        raise e


def delete_todo(td: Todo, conn: Connection) -> bool:
    try:
        query = text("DELETE FROM todos WHERE id = :id")
        conn.execute(query, {"id": td.id})

        return True
    except Exception as e:
        # TODO: Add logging here and consider using specific files and named exceptions
        # for different layers
        raise e
