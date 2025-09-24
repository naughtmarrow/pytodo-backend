import os

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker


def _db_init():
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


class TransactionManager:
    """
    Class that is used to manage database transactions during orchestration of database operations.
    It automatically opens, closes, rollbacks and commits sessions for the user.

    Usage:
        with TransactionManager() as transaction_manager_instance
            some_db_func(...args, transaction_manager_instance)
    """

    def __init__(self):
        self.__session = _SessionLocal()

    def __enter__(self):
        return self.__session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.__session.rollback()
        else:
            self.__session.commit()
        self.__session.close()
