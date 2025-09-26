from src.core import User
from sqlalchemy import Connection, text


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

        id = (
            conn.execute(
                query,
                {
                    "username": user.username,
                    "password": user.password,
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


def get_user_id(user_id: int, conn: Connection) -> User:
    """
    Returns a user object with the requested id from the database.
    Parameters:
        - user_id: An integer corresponding to the id value of a user object in the database
        - conn: A connection to execute queries from
    Returns:
        A user object with the data corresponding to that of the user item in the database.

    Usage:
        user = get_user_id(user_id, conn)
    """
    try:
        query = text("SELECT * FROM users WHERE id = :id")
        usr = conn.execute(query, {"id": user_id}).fetchone()._mapping  # type: ignore

        # WARN: PROBABLY SHOULDN'T BE FETCHING THE PASSWORD UNLESS ABSOLUTELY NECESSARY
        return User(
            id=usr.id,
            username=usr.username,
            password=usr.password,
        )

    except Exception as e:
        # TODO: Add logging here and consider using specific files and named exceptions
        # for different layers
        raise e
    pass

def update_user(user: User, conn: Connection) -> User:
    """
    Updates an already existing user object's values in the database.
    Parameters:
        - user: An object of type Todo to be updated
        - conn: A connection to execute queries from
    Returns:
        A user object with the data corresponding to that of the user item in the database.

    Usage:
        user = update_user(user, conn)
    """
    try:
        query = text(
            "UPDATE users SET username = :username, password = :password "
            + "WHERE id = :id RETURNING *"
        )

        # WARN: PROBABLY SHOULDN'T BE UPDATING THE PASSWORD UNLESS ABSOLUTELY NECESSARY
        res = conn.execute(
            query,
            {
                "id": user.id,
                "username": user.username,
                "password": user.password,
            },
        ).one()._mapping

        return User(**res)
    except Exception as e:
        # TODO: Add logging here and consider using specific files and named exceptions
        # for different layers
        raise e

def delete_user(user: User, conn: Connection) -> bool:
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

        return True
    except Exception as e:
        # TODO: Add logging here and consider using specific files and named exceptions
        # for different layers
        raise e
