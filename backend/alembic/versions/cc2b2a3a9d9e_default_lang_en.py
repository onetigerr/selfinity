"""Set default language_preference to 'en'

Revision ID: cc2b2a3a9d9e
Revises: b9b1f844c5ab
Create Date: 2025-10-12 00:00:00.000000
"""

from __future__ import annotations

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "cc2b2a3a9d9e"
down_revision: Union[str, None] = "b9b1f844c5ab"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Set server default to 'en' for language_preference
    op.execute(
        "ALTER TABLE users ALTER COLUMN "
        "language_preference SET DEFAULT 'en';"
    )


def downgrade() -> None:
    # Revert server default back to 'ru'
    op.execute(
        "ALTER TABLE users ALTER COLUMN "
        "language_preference SET DEFAULT 'ru';"
    )
