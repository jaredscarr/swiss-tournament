"""add round to matches table

Revision ID: 03a46316239b
Revises: c38454a85b1a
Create Date: 2022-06-30 22:09:00.149955

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03a46316239b'
down_revision = 'c38454a85b1a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('matches', sa.Column('round', sa.Integer))


def downgrade():
    op.drop_column('matches', 'round')