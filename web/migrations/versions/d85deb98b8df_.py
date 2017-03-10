"""empty message

Revision ID: d85deb98b8df
Revises: e917766f8de1
Create Date: 2017-03-10 21:43:44.012163

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd85deb98b8df'
down_revision = 'e917766f8de1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('test_result', sa.Column('created_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('test_result', 'created_at')
    # ### end Alembic commands ###