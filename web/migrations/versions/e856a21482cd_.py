"""empty message

Revision ID: e856a21482cd
Revises: 42f92d582713
Create Date: 2017-03-14 21:34:39.095466

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e856a21482cd'
down_revision = '42f92d582713'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('test_plan',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('version', sa.String(length=10), nullable=False),
    sa.Column('source_url', sa.String(), nullable=False),
    sa.Column('summary', sa.Text(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('run_info', sa.Text(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('test_result', 'test_plan')
    op.add_column('test_result', sa.Column('test_plan_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'test_result', 'test_plan', ['test_plan_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('test_result', sa.Column('test_plan', sa.VARCHAR(length=200), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'test_result', type_='foreignkey')
    op.drop_column('test_result', 'test_plan_id')
    op.drop_table('test_plan')
    # ### end Alembic commands ###
