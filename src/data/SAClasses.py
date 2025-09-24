from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, Identity, Index
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)

from src.common.types import PriorityType


class _Base(DeclarativeBase):
    pass


class _SAUser(_Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str]


class _SATodo(_Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(_SAUser.__table__.c.id), nullable=False
    )
    description: Mapped[str]
    date_created: Mapped[datetime]
    date_due: Mapped[Optional[datetime]]
    priority: Mapped[PriorityType]
    completed: Mapped[bool]

    __table_args__ = Index("todo_user_id_fkey", user_id, postgresql_using="hash")
