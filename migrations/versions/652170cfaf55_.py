"""empty message

Revision ID: 652170cfaf55
Revises: 8c68b066b7e6
Create Date: 2020-10-17 11:32:01.439857

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '652170cfaf55'
down_revision = '8c68b066b7e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('results', sa.Column('result', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.drop_column('results', 'result_all')
    op.drop_column('results', 'result_no_stop_words')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('results', sa.Column('result_no_stop_words', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True))
    op.add_column('results', sa.Column('result_all', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True))
    op.drop_column('results', 'result')
    # ### end Alembic commands ###
