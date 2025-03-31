"""Add a column

Revision ID: 80ffb6696d77
Revises: 61bd87c5acb8
Create Date: 2025-03-21 15:26:11.451585

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '80ffb6696d77'
down_revision: Union[str, None] = '61bd87c5acb8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('account', sa.Column('last_transaction_date', sa.DateTime(), nullable=True)
                  )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('account', 'last_transaction_date')
