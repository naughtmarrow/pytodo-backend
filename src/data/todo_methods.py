from typing import List

from src.core import Todo
from . import TransactionManager

def save_todo(td: Todo, tm: TransactionManager) -> int: #type: ignore
    pass

def get_todo_id(todo_id: int, tm: TransactionManager) -> Todo: #type: ignore
    pass

def get_todos_from_user(user_id: int, tm: TransactionManager) -> List[Todo]: #type: ignore
    pass

def update_todo(td: Todo, tm: TransactionManager) -> int: #type: ignore
    pass

def delete_todo(todo_id: int, tm: TransactionManager) -> bool: #type: ignore
    return True
