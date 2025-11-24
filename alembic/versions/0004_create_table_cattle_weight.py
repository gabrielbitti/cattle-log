"""create table cattle_weight

Revision ID: 0004
Revises: 0003
Create Date: 2025-11-24 20:47:38.786256

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0004'
down_revision: Union[str, None] = '0003'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('cattle_weight',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('cattle_id', sa.Integer(), nullable=False),
        sa.Column('weight', sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column('measurement_date', sa.Date(), nullable=False),
        sa.Column('notes', sa.String(), nullable=True),
        sa.Column('created_at', sa.Date(), nullable=False),
        sa.Column('updated_at', sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(['cattle_id'], ['cattle.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cattle_weight_id'), 'cattle_weight', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_cattle_weight_id'), table_name='cattle_weight')
    op.drop_table('cattle_weight')
