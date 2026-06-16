"""Create posts table

Revision ID: f5d1ee0f5b88
Revises: 
Create Date: 2026-06-16 10:16:03.016647

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5d1ee0f5b88'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("posts",sa.Column("id",sa.Integer(),nullable=False,primary_key=True),sa.Column("title",sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
