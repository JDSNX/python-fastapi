"""add content column to posts table

Revision ID: 31125fa7feab
Revises: 8e4db93c1da0
Create Date: 2022-12-07 16:55:50.913070

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31125fa7feab'
down_revision = '8e4db93c1da0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
