"""add user table

Revision ID: 61c992792a68
Revises: 31125fa7feab
Create Date: 2022-12-07 17:00:23.336667

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61c992792a68'
down_revision = '31125fa7feab'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                            server_default=sa.text('now()') ,nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
