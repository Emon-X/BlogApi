"""Add is_admin field to users and set defaults

Revision ID: 211308c411ba
Revises: e9a50454824d
Create Date: 2026-05-08 16:28:58.066775

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '211308c411ba'
down_revision: Union[str, Sequence[str], None] = 'e9a50454824d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Update any NULL is_admin values to False
    op.execute("UPDATE users SET is_admin = FALSE WHERE is_admin IS NULL")
    # Add NOT NULL constraint
    op.alter_column('users', 'is_admin', existing_type=sa.Boolean(), nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Remove NOT NULL constraint
    op.alter_column('users', 'is_admin', existing_type=sa.Boolean(), nullable=True)
