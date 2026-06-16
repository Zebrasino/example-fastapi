"""Add columns to posts table

Revision ID: 4b21cf999731
Revises: a0ed60be7da8
Create Date: 2026-06-16 10:56:35.310107

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b21cf999731'
down_revision: Union[str, Sequence[str], None] = 'a0ed60be7da8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts",sa.Column("published",sa.Boolean(),server_default=sa.text("TRUE"),nullable=False))
    op.add_column("posts",sa.Column("created_at",sa.TIMESTAMP(timezone=True),server_default=sa.text("now()"),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts","published")
    op.drop_column("posts","created_at")
    pass
