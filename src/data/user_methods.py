from src.core import User
from . import TransactionManager

def save_user(usr: User, tm: TransactionManager) -> int: #type: ignore
    pass

def get_user_id(user_id: int, tm: TransactionManager) -> User: #type: ignore
    pass

def update_username(usr: User, tm: TransactionManager) -> int: #type: ignore
    pass

def update_password(usr: User, tm: TransactionManager) -> int: #type: ignore
    pass

def delete_user(user_id: int, tm: TransactionManager) -> bool: #type: ignore
    return True
