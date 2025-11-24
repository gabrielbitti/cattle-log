"""create table cattle_reproduction

Revision ID: 0003
Revises: 0002
Create Date: 2025-11-24 20:46:21.659303

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0003'
down_revision: Union[str, None] = '0002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('cattle_reproduction',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('cattle_id', sa.Integer(), nullable=False),
        sa.Column('event_type', sa.Enum('MATING', 'PREGNANCY_CHECK', 'BIRTH', 'ABORTION', 'WEANING', name='reproductive_event_enum'), nullable=False),
        sa.Column('event_date', sa.Date(), nullable=False),
        sa.Column('partner_id', sa.Integer(), nullable=True),
        sa.Column('offspring_id', sa.Integer(), nullable=True),
        sa.Column('pregnancy_confirmed', sa.Boolean(), nullable=True),
        sa.Column('expected_birth_date', sa.Date(), nullable=True),
        sa.Column('notes', sa.String(), nullable=True),
        sa.Column('created_at', sa.Date(), nullable=False),
        sa.Column('updated_at', sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(['cattle_id'], ['cattle.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['offspring_id'], ['cattle.id'], ),
        sa.ForeignKeyConstraint(['partner_id'], ['cattle.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cattle_reproduction_id'), 'cattle_reproduction', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_cattle_reproduction_id'), table_name='cattle_reproduction')
    op.drop_table('cattle_reproduction')
    op.execute("DROP TYPE reproductive_event_enum;")
