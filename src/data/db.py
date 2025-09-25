import os

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text
from sqlalchemy.orm import sessionmaker


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
_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


def ping_db() -> bool:
    """
    Used to ping the database in order to test the connection
    """
    try:
        with _engine.connect() as conn:
            _ = conn.execute(text("SELECT 1"))
    except Exception as e:
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
        with TransactionManager() as transaction_manager_instance
            some_db_func(...args, transaction_manager_instance)
        In DAL:
        tm._session()
    """

    def __init__(self, debug: bool = False):
        self.__session = _SessionLocal()
        self.__session.execute(text("SET search_path TO :schema"), {"schema": os.getenv('DB_SCHEMA')})
        self.__debug = debug

    def __enter__(self):
        return self.__session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or self.__debug:
            self.__session.rollback()
        else:
            self.__session.commit()
        self.__session.close()

    @property
    def _session(self):
        """Allows direct access to the session for usage. You should only use while in DAL methods"""
        return self.__session
