import os

from dotenv import load_dotenv
from sqlalchemy import Connection, URL, create_engine, text


def _db_init():
    load_dotenv()
    url = URL.create(
        "postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
    )

    return create_engine(
        url,
        connect_args={"options": f"-csearch_path={os.getenv('DB_SCHEMA')}"},
        pool_pre_ping=True,
        echo=True,
    )


_engine = _db_init()

def ping_db() -> bool:
    """
    Used to ping the database in order to test the connection.
    Returns true if connection is successful and raises an exception if the connection fails
    """
    try:
        with _engine.connect() as conn:
            _ = conn.execute(text("SELECT 1"))
    except Exception as e:
        # TODO: change to a normal logging setup
        print(f"Database ping failed: {e}")
        return False
    else:
        print("Database connection succesful")
        return True


class TransactionManager:
    """
    Class that is used to manage database transactions during orchestration of database operations.
    It automatically opens, closes, rollbacks and commits sessions for the user.

    Usage:
        In BL:
        The transaction manager connection is passed to other methods for querying.
            with TransactionManager() as tm:
                some_db_method(...args, transaction_manager=tm)

        In DAL:
        The connection can be used as usual.
            tm.execute(text("SOME SQL QUERY"))
    """

    def __init__(self, debug: bool = False):
        self.__connection = Connection(_engine)
        self.__connection.execute(text("SET search_path TO :schema"), {"schema": os.getenv('DB_SCHEMA')})
        self.__debug = debug

    def __enter__(self):
        return self.__connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or self.__debug:
            self.__connection.rollback()
        else:
            self.__connection.commit()
        self.__connection.close()
