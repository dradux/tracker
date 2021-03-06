"""added 'target server quantity' to test results

Revision ID: fa14c4b40d9e
Revises: 0a40b3785b2d
Create Date: 2017-05-26 09:55:30.616046

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa14c4b40d9e'
down_revision = '0a40b3785b2d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('test_result', sa.Column('target_server_quantity', sa.String(length=10), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('test_result', 'target_server_quantity')
    # ### end Alembic commands ###
