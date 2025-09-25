import pytest
from src.data import TransactionManager, ping_db, save_todo, get_todo_id, get_todos_from_user, delete_todo, save_user, get_user_id, delete_user, update_user
from src.core import Todo, User


def test_db_ping():
    assert ping_db()

def test_user_save():
    try:
        with TransactionManager(debug=True) as conn:
            default_username = "test_username"
            default_password = "test_password"

            usr = User(
                id=None,
                username=default_username,
                password=default_password
            )
            usr_id = save_user(usr, conn)

            get_usr = get_user_id(usr_id, conn)

            assert(get_usr.id is not None)
            assert(get_usr.username == usr.username)
            assert(get_usr.password == usr.password)

            update_username="test_username_update"
            usr.username = update_username

            usr.id = usr_id
            upd_usr = update_user(usr, conn)

            assert(upd_usr.username == update_username)

            get_usr = get_user_id(upd_usr.id, conn)

            assert(get_usr.username == usr.username)

    except Exception as e:
        raise e

def test_user_delete():
    with pytest.raises(Exception):
        with TransactionManager(debug=True) as conn:
            default_username = "test_username_del"
            default_password = "test_password_del"
            usr = User(
                id=None,
                username=default_username,
                password=default_password
            )
            usr_id = save_user(usr, conn)

            get_usr = get_user_id(usr_id, conn)

            assert(get_usr.id is not None)
            assert(get_usr.username == usr.username)
            assert(get_usr.password == usr.password)

            assert(delete_user(usr, conn))

            get_usr = get_user_id(usr_id, conn)
            assert(get_usr.id is None)
