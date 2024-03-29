"""empty message

Revision ID: 3711ded84f7d
Revises: 
Create Date: 2019-11-14 22:19:50.079221

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3711ded84f7d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('auth_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=40), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('first_name', sa.String(length=40), nullable=True),
    sa.Column('last_name', sa.String(length=80), nullable=True),
    sa.Column('phone_number', sa.String(length=14), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('registration_date', sa.DateTime(), nullable=True),
    sa.Column('last_login_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('auth_user')
    # ### end Alembic commands ###
