"""Create retweets table

Revision ID: 8a7b9a1c2d3e
Revises: 0667e42621bb
Create Date: 2026-06-17 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8a7b9a1c2d3e"
down_revision: Union[str, Sequence[str], None] = "0667e42621bb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "retweets",
        sa.Column("id_user", sa.Integer(), nullable=False),
        sa.Column("id_post", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["id_post"], ["posts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["id_user"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id_user", "id_post"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("retweets")
