"""empty message

Revision ID: 41ee8626d04f
Revises: 
Create Date: 2018-06-06 21:25:31.817657

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41ee8626d04f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('t_letter',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('t_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=50), nullable=True),
    sa.Column('nickName', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('phone', sa.String(length=12), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_life', sa.Boolean(), nullable=True),
    sa.Column('regist_time', sa.DateTime(), nullable=True),
    sa.Column('last_login_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('t_city',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('parentId', sa.Integer(), nullable=True),
    sa.Column('regionName', sa.String(length=20), nullable=True),
    sa.Column('cityCode', sa.Integer(), nullable=True),
    sa.Column('pinYin', sa.String(length=50), nullable=True),
    sa.Column('letter_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['letter_id'], ['t_letter.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('t_city')
    op.drop_table('t_user')
    op.drop_table('t_letter')
    # ### end Alembic commands ###
