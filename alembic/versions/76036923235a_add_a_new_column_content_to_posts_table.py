"""Add a new column content to posts table

Revision ID: 76036923235a
Revises: f5d1ee0f5b88
Create Date: 2026-06-16 10:31:34.339538

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '76036923235a'
down_revision: Union[str, Sequence[str], None] = 'f5d1ee0f5b88'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("content",sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts","content")
    pass
