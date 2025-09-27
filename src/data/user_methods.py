import logging

from psycopg2.errors import NoData
from sqlalchemy import Connection, text

from src.core import User

_logger = logging.getLogger("USERDAL")


def save_user(user: User, conn: Connection) -> int:
    """
    Saves a user object in the database.
    Parameters:
        - user: An object of type User to be saved
        - conn: A connection to execute queries from
    Returns:
        The primary key (id) of the inserted user object in the database.

    Usage:
        new_id = save_user(user, conn)
    """
    try:
        query = text(
            "INSERT INTO users (username, password)"
            + "VALUES (:username, :password) RETURNING id"
        )
        # it's probably fine to take the password here since we are creating the user
        res = (
            conn.execute(
                query,
                {
                    "username": user.username,
                    "password": user.password,
                },
            )
            .one()
        )

        if res is None:
            raise Exception("User create responds with no data")

        id = res.id
        return id

    except Exception as e:
        _logger.error(msg=f"Error while saving user: {e}")
        raise e


# minus password cause we don't want the password running around everywhere
def get_user_id(user_id: int, conn: Connection) -> User:
    """
    Returns a user object (minus password) with the requested id from the database.
    Parameters:
        - user_id: An integer corresponding to the id value of a user object in the database
        - conn: A connection to execute queries from
    Returns:
        A user object with the data corresponding to that of the user item in the database (minus password).

    Usage:
        user = get_user_id(user_id, conn)
    """
    try:
        query = text("SELECT * FROM users WHERE id = :id")
        usr = conn.execute(query, {"id": user_id}).fetchone()

        # HACK: this really can't be the best way to deal with this lmao
        if usr is None:
            raise NoData

        usr = usr._mapping  # type: ignore

        return User(
            id=usr.id,
            username=usr.username,
            password=None
        )

    except Exception as e:
        _logger.error(msg=f"Error while fetching user from id: {e}")
        raise e
    pass


def get_user_password(user_id: int, conn: Connection) -> str:
    """
    Returns a user's password with the requested id from the database for login.
    Parameters:
        - user_id: An integer corresponding to the id value of a user object in the database
        - conn: A connection to execute queries from
    Returns:
        A user object with the data corresponding to that of the user item in the database (minus password).

    Usage:
        user = get_user_id(user_id, conn)
    """
    try:
        query = text("SELECT users.password FROM users WHERE id = :id")
        res = conn.execute(query, {"id": user_id}).fetchone()

        # HACK: this really can't be the best way to deal with this lmao
        if res is None:
            raise NoData

        password = res.password  # type: ignore

        return password

    except Exception as e:
        _logger.error(msg=f"Error while fetching user from id: {e}")
        raise e
    pass


def update_user(user: User, conn: Connection) -> int:
    """
    Updates an already existing user object's values (minus password) in the database.
    Parameters:
        - user: An object of type Todo to be updated
        - conn: A connection to execute queries from
    Returns:
        An id corresponding to the the user item in the database.

    Usage:
        user = update_user(user, conn)
    """
    try:
        query = text(
            "UPDATE users SET username = :username "
            + "WHERE id = :id RETURNING id"
        )

        res = (
            conn.execute(
                query,
                {
                    "id": user.id,
                    "username": user.username,
                },
            )
            .one()
        )

        if res is None:
            raise Exception("User create responds with no data")

        id = res.id
        return id
    except Exception as e:
        _logger.error(msg=f"Error while updating user: {e}")
        raise e

# seperated the update for the password because we don't wanna have the password on the backend more than needed
def update_user_password(user: User, conn: Connection) -> int:
    """
    Updates an already existing user object's password in the database.
    Parameters:
        - user: An object of type Todo to be updated
        - conn: A connection to execute queries from
    Returns:
        An id corresponding to the the user item in the database.

    Usage:
        user = update_user_password(user, conn)
    """
    try:
        query = text(
            "UPDATE users SET password = :password "
            + "WHERE id = :id RETURNING id"
        )

        res = (
            conn.execute(
                query,
                {
                    "id": user.id,
                    "password": user.password,
                },
            )
            .one()
        )

        if res is None:
            raise Exception("User create responds with no data")

        id = res.id
        return id
    except Exception as e:
        _logger.error(msg=f"Error while updating user: {e}")
        raise e



def delete_user(user: User, conn: Connection):
    """
    Deletes a user item from the database.
    Parameters:
        - user: An object of type Todo to be deleted
        - conn: A connection to execute queries from
        A boolean value to represent the success of the operation.

    Usage:
        user = delete_user(user, conn)
    """
    try:
        query = text("DELETE FROM users WHERE id = :id")
        conn.execute(query, {"id": user.id})

    except Exception as e:
        _logger.error(msg=f"Error while deleting user: {e}")
        raise e
