from src.core import User
from sqlalchemy import Connection, text


def save_user(usr: User, conn: Connection) -> User:
    try:
        query = text(
            "INSERT INTO users (username, password)"
            + "VALUES (:username, :password) RETURNING id"
        )

        id = (
            conn.execute(
                query,
                {
                    "username": usr.username,
                    "password": usr.password,
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
    try:
        query = text("DELETE FROM users WHERE id = :id")
        conn.execute(query, {"id": user.id})

        return True
    except Exception as e:
        # TODO: Add logging here and consider using specific files and named exceptions
        # for different layers
        raise e
