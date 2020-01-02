"""empty message

Revision ID: ee838499704e
Revises: 9153989d7abb
Create Date: 2020-01-02 22:20:13.096242

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee838499704e'
down_revision = '9153989d7abb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('CommenterID', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'comment', 'member', ['CommenterID'], ['ID'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.drop_column('comment', 'CommenterID')
    # ### end Alembic commands ###