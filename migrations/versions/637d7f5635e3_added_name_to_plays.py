"""Added name to plays

Revision ID: 637d7f5635e3
Revises: bf9d0c81ecde
Create Date: 2022-04-07 14:35:53.297023

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '637d7f5635e3'
down_revision = 'bf9d0c81ecde'
branch_labels = None
depends_on = None


def upgrade():
    try:
        # ### commands auto generated by Alembic - please adjust! ###
        op.add_column('play', sa.Column('name', sa.String(length=256), nullable=False))
        # ### end Alembic commands ###
    except sa.exc.OperationalError:
        pass


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('play', 'name')
    # ### end Alembic commands ###
