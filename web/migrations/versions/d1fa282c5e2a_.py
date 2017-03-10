"""empty message

Revision ID: d1fa282c5e2a
Revises: d85deb98b8df
Create Date: 2017-03-10 21:54:52.491489

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1fa282c5e2a'
down_revision = 'd85deb98b8df'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('server', sa.Column('creator_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'server', 'user', ['creator_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'server', type_='foreignkey')
    op.drop_column('server', 'creator_id')
    # ### end Alembic commands ###
