"""empty message

Revision ID: e7e408978779
Revises: 8cada5e2669b
Create Date: 2017-03-14 22:11:02.669613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7e408978779'
down_revision = '8cada5e2669b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('test_plan', 'description',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('test_plan', 'run_info',
               existing_type=sa.TEXT(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('test_plan', 'run_info',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('test_plan', 'description',
               existing_type=sa.TEXT(),
               nullable=True)
    # ### end Alembic commands ###
