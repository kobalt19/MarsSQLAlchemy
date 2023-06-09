"""Attempt №2

Revision ID: 45c79b2eb37c
Revises: 25299d88fbad
Create Date: 2023-04-28 22:00:56.572835

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45c79b2eb37c'
down_revision = '25299d88fbad'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('departments',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('chief_id', sa.Integer(), nullable=True),
    sa.Column('members', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['chief_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('departments')
    # ### end Alembic commands ###
