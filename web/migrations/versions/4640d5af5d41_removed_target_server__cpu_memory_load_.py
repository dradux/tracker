"""removed target_server_[cpu/memory/load] from model as they are no longer needed

Revision ID: 4640d5af5d41
Revises: 70d7bfcbd8a6
Create Date: 2017-04-15 19:26:38.197114

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4640d5af5d41'
down_revision = '70d7bfcbd8a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('test_result', 'target_server_cpu')
    op.drop_column('test_result', 'target_server_memory')
    op.drop_column('test_result', 'target_server_load')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('test_result', sa.Column('target_server_load', sa.NUMERIC(precision=5, scale=2), autoincrement=False, nullable=True))
    op.add_column('test_result', sa.Column('target_server_memory', sa.NUMERIC(precision=5, scale=2), autoincrement=False, nullable=True))
    op.add_column('test_result', sa.Column('target_server_cpu', sa.NUMERIC(precision=5, scale=2), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
