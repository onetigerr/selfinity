"""my migration

Revision ID: a69908bd1a96
Revises: d25bf845a0b3
Create Date: 2025-10-10 16:49:51.314399

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a69908bd1a96'
down_revision: Union[str, None] = 'd25bf845a0b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # No-op placeholder to preserve migration history.
    pass


def downgrade() -> None:
    # No-op placeholder to preserve migration history.
    pass

