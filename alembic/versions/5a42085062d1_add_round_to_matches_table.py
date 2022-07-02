"""add round to matches table

Revision ID: 5a42085062d1
Revises: 4eb1c8a6f0bc
Create Date: 2022-06-30 21:35:45.087620

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a42085062d1'
down_revision = '4eb1c8a6f0bc'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('matches', sa.Column('round', sa.Integer))


def downgrade():
    op.drop_column('matches', 'round')
