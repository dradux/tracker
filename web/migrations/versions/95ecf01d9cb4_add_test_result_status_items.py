"""add test_result_status items

Revision ID: 95ecf01d9cb4
Revises: ea71f73f5460
Create Date: 2017-03-29 19:41:26.581925

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95ecf01d9cb4'
down_revision = 'ea71f73f5460'
branch_labels = None
depends_on = None


def upgrade():
    #~ op.bulk_insert('test_result_status',
        #~ [
            #~ {'status': 'Created'},
            #~ {'status': 'Completed'},
            #~ {'status': 'Failed'}
        #~ ]
    #~ )
    op.execute("INSERT INTO test_result_status (status) VALUES ('Created')")
    op.execute("INSERT INTO test_result_status (status) VALUES ('Completed')")
    op.execute("INSERT INTO test_result_status (status) VALUES ('Failed')")

    op.execute("UPDATE test_result SET status_id=(SELECT id FROM test_result_status where status='Created') WHERE test_passed is null")
    op.execute("UPDATE test_result SET status_id=(SELECT id FROM test_result_status where status='Completed') WHERE test_passed=true")
    op.execute("UPDATE test_result SET status_id=(SELECT id FROM test_result_status where status='Failed') WHERE test_passed=false")


def downgrade():
    op.execute("delete from test_result_status where status in('Created', 'Completed', 'Failed')")
