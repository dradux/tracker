"""empty message

Revision ID: 3b47d4c0d528
Revises: 46b94eb5a1a6
Create Date: 2017-03-10 22:20:12.301275

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b47d4c0d528'
down_revision = '46b94eb5a1a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('test_result', sa.Column('creator_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'test_result', 'user', ['creator_id'], ['id'])
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.drop_constraint(None, 'test_result', type_='foreignkey')
    op.drop_column('test_result', 'creator_id')
    # ### end Alembic commands ###
