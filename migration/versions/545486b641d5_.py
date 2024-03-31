"""empty message

Revision ID: 545486b641d5
Revises: 
Create Date: 2024-03-29 22:06:03.794642

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '545486b641d5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('type_point',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('notation', sa.String(length=4), nullable=False),
    sa.Column('type_data', sa.String(length=10), nullable=False),
    sa.Column('description', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('type_user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('description', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('uuid', sa.UUID(), nullable=True),
    sa.Column('login', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('id_type', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_type'], ['type_user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('login'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('point',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=True),
    sa.Column('id_type_point', sa.Integer(), nullable=True),
    sa.Column('value', sa.String(), nullable=False),
    sa.Column('default_value', sa.String(), nullable=True),
    sa.Column('datareg', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['id_type_point'], ['type_point.id'], ),
    sa.ForeignKeyConstraint(['id_user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('point')
    op.drop_table('user')
    op.drop_table('type_user')
    op.drop_table('type_point')
    # ### end Alembic commands ###