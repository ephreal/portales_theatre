"""Added pricing to reservation object

Revision ID: c83557b4ca84
Revises: 8ff9f55e0cd3
Create Date: 2022-04-15 20:57:57.283358

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c83557b4ca84'
down_revision = '8ff9f55e0cd3'
branch_labels = None
depends_on = None


def upgrade():
    try:
        # ### commands auto generated by Alembic - please adjust! ###
        op.add_column('reservation', sa.Column('price', sa.Integer(), nullable=False))
        # ### end Alembic commands ###
    except sa.exc.OperationalError:
        pass


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reservation', 'price')
    # ### end Alembic commands ###
