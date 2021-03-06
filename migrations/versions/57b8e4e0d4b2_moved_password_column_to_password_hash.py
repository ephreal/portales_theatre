"""Moved password column to password hash

Revision ID: 57b8e4e0d4b2
Revises: d2fb2c1fd31d
Create Date: 2022-04-12 13:22:48.303471

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '57b8e4e0d4b2'
down_revision = 'd2fb2c1fd31d'
branch_labels = None
depends_on = None


def upgrade():
    try:
        # ### commands auto generated by Alembic - please adjust! ###
        op.add_column('user', sa.Column('password_hash', sa.String(length=128), nullable=True))
        op.drop_column('user', 'password')
        # ### end Alembic commands ###
    except sa.exc.OperationalError:
        pass


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=128), nullable=True))
    op.drop_column('user', 'password_hash')
    # ### end Alembic commands ###
