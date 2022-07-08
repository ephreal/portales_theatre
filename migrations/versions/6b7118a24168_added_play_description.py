"""Added play description

Revision ID: 6b7118a24168
Revises: 637d7f5635e3
Create Date: 2022-04-07 14:37:42.999953

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b7118a24168'
down_revision = '637d7f5635e3'
branch_labels = None
depends_on = None


def upgrade():
    try:
        # ### commands auto generated by Alembic - please adjust! ###
        op.add_column('play', sa.Column('description', sa.String(length=4096), nullable=True))
        # ### end Alembic commands ###
    except sa.exc.OperationalError:
        pass


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('play', 'description')
    # ### end Alembic commands ###