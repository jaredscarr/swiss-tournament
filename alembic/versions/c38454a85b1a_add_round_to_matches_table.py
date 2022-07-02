"""add round to matches table

Revision ID: c38454a85b1a
Revises: 5a42085062d1
Create Date: 2022-06-30 22:00:28.362731

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c38454a85b1a'
down_revision = '5a42085062d1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('matches', sa.Column('round', sa.Integer))


def downgrade():
    op.drop_column('matches', 'round')
