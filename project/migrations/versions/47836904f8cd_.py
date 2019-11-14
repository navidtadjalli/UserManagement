"""empty message

Revision ID: 47836904f8cd
Revises: 
Create Date: 2019-11-14 13:59:36.910298

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47836904f8cd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blog_post')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blog_post',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=80), nullable=True),
    sa.Column('description', sa.TEXT(), nullable=True),
    sa.Column('author_id', sa.INTEGER(), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('modified_at', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['auth_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###