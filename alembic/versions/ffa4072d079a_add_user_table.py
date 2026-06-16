"""Add user table

Revision ID: ffa4072d079a
Revises: 76036923235a
Create Date: 2026-06-16 10:38:46.191813

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ffa4072d079a'
down_revision: Union[str, Sequence[str], None] = '76036923235a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("users", sa.Column("id",sa.Integer(),nullable=False,primary_key=True),
                    sa.Column("email",sa.String(),nullable=False,unique=True),sa.Column("password",sa.String(),nullable=False),
                    sa.Column("created_at",sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text("now()")))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
    pass
