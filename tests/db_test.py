from datetime import datetime
from typing import List

import pytest

from src.common import PriorityType

from src.data import TransactionManager, ping_db, save_todo, get_todo_id, get_todos_from_user, delete_todo, save_user, get_user_id, delete_user, update_user
from src.core import Todo, User


def test_db_ping():
    assert ping_db()


@pytest.fixture
def std_user() -> User:
    return User(id=None, username="test_username", password="test_password")


@pytest.fixture
def std_todo() -> Todo:
    return Todo(
        id=None,
        user_id=1,
        description="This is a todo",
        date_created=datetime.now(),
        date_due=datetime.now(),
        priority=PriorityType.IMPORTANT,
        completed=False,
    )

@pytest.fixture
def std_todo_list() -> List[Todo]:
    td1: Todo = Todo(
        id=None,
        user_id=1,
        description="This is a todo",
        date_created=datetime.now(),
        date_due=datetime.now(),
        priority=PriorityType.IMPORTANT,
        completed=False,
    )

    td2: Todo = Todo(
        id=None,
        user_id=1,
        description="This is another todo",
        date_created=datetime.now(),
        date_due=datetime.now(),
        priority=PriorityType.IMPORTANT,
        completed=False,
    )

    td3: Todo = Todo(
        id=None,
        user_id=1,
        description="This is yet another todo",
        date_created=datetime.now(),
        date_due=datetime.now(),
        priority=PriorityType.IMPORTANT,
        completed=False,
    )

    tdlist: List[Todo] = []
    tdlist.append(td1)
    tdlist.append(td2)
    tdlist.append(td3)

    return tdlist

def test_user_save(std_user):
    try:
        with TransactionManager(debug=True) as conn:
            usr_id = save_user(std_user, conn)

            get_usr = get_user_id(usr_id, conn)

            assert get_usr.id is not None
            assert get_usr.username == std_user.username
            assert get_usr.password == std_user.password

            update_username = "test_username_update"
            std_user.username = update_username

            std_user.id = usr_id
            upd_usr = update_user(std_user, conn)

            assert upd_usr.username == update_username

            get_usr = get_user_id(upd_usr.id, conn)

            assert get_usr.username == std_user.username

    except Exception as e:
        raise e


def test_user_delete(std_user):
    with pytest.raises(Exception):
        with TransactionManager(debug=True) as conn:
            usr_id = save_user(std_user, conn)

            get_usr = get_user_id(usr_id, conn)

            assert get_usr.id is not None
            assert get_usr.username == std_user.username
            assert get_usr.password == std_user.password

            assert delete_user(std_user, conn)

            get_usr = get_user_id(usr_id, conn)
            assert get_usr.id is None


def test_todo_save(std_user, std_todo):
    try:
        with TransactionManager(debug=True) as conn:
            usr_id = save_user(std_user, conn)
            std_todo.user_id = usr_id

            todo_id = save_todo(std_todo, conn)
            std_todo.id = todo_id

            get_todo = get_todo_id(todo_id, conn)

            assert(get_todo == std_todo)
    except Exception as e:
        raise e

def test_todo_list_fetch(std_user, std_todo_list):
    try:
        with TransactionManager(debug=True) as conn:
            user_id = save_user(std_user, conn)

            for x in std_todo_list:
                x.user_id = user_id
                td_id = save_todo(x, conn)
                x.id = td_id

            fetched_todo_list = get_todos_from_user(user_id, conn)

            assert all(x == y for x, y in zip(std_todo_list, fetched_todo_list))
    except Exception as e:
        raise e

def test_delete_todo(std_user, std_todo):
    try:
        with TransactionManager(debug=True) as conn:
            usr_id = save_user(std_user, conn)
            std_todo.user_id = usr_id

            todo_id = save_todo(std_todo, conn)
            std_todo.id = todo_id

            delete_todo(std_todo, conn)

    except Exception as e:
        raise e
