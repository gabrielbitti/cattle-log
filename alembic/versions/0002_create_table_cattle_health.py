"""create table cattle_health

Revision ID: 0002
Revises: 0001
Create Date: 2025-11-24 20:38:42.618398

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
    op.create_table('cattle_health',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('cattle_id', sa.Integer(), nullable=False),
        sa.Column('record_type', sa.Enum('VACCINATION', 'DISEASE', 'INJURY', 'TREATMENT', 'CHECKUP', name='health_record_type_enum'), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('veterinarian', sa.String(), nullable=True),
        sa.Column('medication', sa.String(), nullable=True),
        sa.Column('dosage', sa.String(), nullable=True),
        sa.Column('cost', sa.DECIMAL(precision=10, scale=2), nullable=True),
        sa.Column('next_dose_date', sa.Date(), nullable=True),
        sa.Column('notes', sa.String(), nullable=True),
        sa.Column('created_at', sa.Date(), nullable=False),
        sa.Column('updated_at', sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(['cattle_id'], ['cattle.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cattle_health_id'), 'cattle_health', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_cattle_health_id'), table_name='cattle_health')
    op.drop_table('cattle_health')
    op.execute("DROP TYPE health_record_type_enum;")
