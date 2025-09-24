"""Initial Migration

Revision ID: 05b6db1ca1f3
Revises:
Create Date: 2025-09-24 01:42:26.195369

"""

import os
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from dotenv import load_dotenv

# revision identifiers, used by Alembic.
revision: str = "05b6db1ca1f3"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

load_dotenv()
schema = os.getenv("DB_SCHEMA")


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    conn.execute(sa.text("SET search_path TO :schema"), {"schema": schema})

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), sa.Identity(always=True), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
        if_not_exists=True,
    )
    op.create_table(
        "todos",
        sa.Column("id", sa.Integer(), sa.Identity(always=True), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("date_created", sa.DateTime(), nullable=False),
        sa.Column("date_due", sa.DateTime(), nullable=True),
        sa.Column(
            "priority",
            sa.Enum("URGENT", "IMPORTANT", "NORMAL", "OPTIONAL", name="prioritytype"),
            nullable=False,
        ),
        sa.Column("completed", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        if_not_exists=True,
    )
    op.create_index(
        "todo_user_id_fkey",
        "todos",
        ["user_id"],
        unique=False,
        postgresql_using="hash",
    )


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()
    conn.execute(sa.text("SET search_path TO :schema"), {"schema": schema})

    op.drop_index("todo_user_id_fkey", table_name="todos", postgresql_using="hash")
    op.drop_table("todos")
    op.drop_table("users")
