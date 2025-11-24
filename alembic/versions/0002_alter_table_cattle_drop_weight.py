"""alter_table_cattle_drop_weight

Revision ID: 0002
Revises: 0001
Create Date: 2025-11-24 20:14:07.076255

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0002'
down_revision: Union[str, None] = '0001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column('cattle', 'weight')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        'cattle',
        sa.Column('weight', sa.NUMERIC(precision=10, scale=2),
                  autoincrement=False,
                  nullable=True)
    )
