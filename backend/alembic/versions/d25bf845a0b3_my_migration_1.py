"""my migration 1

Revision ID: d25bf845a0b3
Revises: 0001_initial
Create Date: 2025-10-10 16:47:31.321009

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd25bf845a0b3'
down_revision: Union[str, None] = '0001_initial'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # No-op placeholder to preserve migration history.
    pass


def downgrade() -> None:
    # No-op placeholder to preserve migration history.
    pass

