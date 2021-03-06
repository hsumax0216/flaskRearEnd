"""empty message

Revision ID: 89b08346afb2
Revises: ee838499704e
Create Date: 2020-01-03 14:27:38.973838

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89b08346afb2'
down_revision = 'ee838499704e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('member', sa.Column('VerificationCode', sa.VARCHAR(length=6), nullable=False))
    op.add_column('member', sa.Column('VerificationStatus', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('member', 'VerificationStatus')
    op.drop_column('member', 'VerificationCode')
    # ### end Alembic commands ###
