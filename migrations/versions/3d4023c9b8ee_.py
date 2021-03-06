"""empty message

Revision ID: 3d4023c9b8ee
Revises: 1e577f33da08
Create Date: 2018-06-07 15:12:00.348084

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d4023c9b8ee'
down_revision = '1e577f33da08'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('t_user', sa.Column('photo_1', sa.String(length=100), nullable=True))
    op.add_column('t_user', sa.Column('photo_2', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('t_user', 'photo_2')
    op.drop_column('t_user', 'photo_1')
    # ### end Alembic commands ###
