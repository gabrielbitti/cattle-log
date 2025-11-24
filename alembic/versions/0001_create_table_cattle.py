"""create table cattle

Revision ID: 0001
Revises: 
Create Date: 2025-11-24 20:27:28.927291

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('cattle',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('identification', sa.String(), nullable=True),
        sa.Column('race', sa.String(), nullable=False),
        sa.Column('gender', sa.Enum('MALE', 'FEMALE', name='gender_enum'), nullable=False),
        sa.Column('birth_date', sa.Date(), nullable=True),
        sa.Column('acquisition_date', sa.Date(), nullable=True),
        sa.Column('acquisition_value', sa.DECIMAL(precision=10, scale=2), nullable=True),
        sa.Column('status', sa.Enum('ACTIVE', 'SOLD', 'DECEASED', 'TRANSFERRED', name='status_enum'), nullable=False),
        sa.Column('mother_id', sa.Integer(), nullable=True),
        sa.Column('father_id', sa.Integer(), nullable=True),
        sa.Column('origin', sa.String(), nullable=True),
        sa.Column('notes', sa.String(), nullable=True),
        sa.Column('created_at', sa.Date(), nullable=False),
        sa.Column('updated_at', sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(['father_id'], ['cattle.id'], ),
        sa.ForeignKeyConstraint(['mother_id'], ['cattle.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('identification')
    )
    op.create_index(op.f('ix_cattle_id'), 'cattle', ['id'], unique=False)
    op.create_index(op.f('ix_cattle_race'), 'cattle', ['race'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_cattle_race'), table_name='cattle')
    op.drop_index(op.f('ix_cattle_id'), table_name='cattle')
    op.drop_table('cattle')
    op.execute("DROP TYPE gender_enum;")
    op.execute("DROP TYPE status_enum;")
