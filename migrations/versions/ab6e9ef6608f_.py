"""empty message

Revision ID: ab6e9ef6608f
Revises: 1671e78f512d
Create Date: 2019-07-25 23:05:49.444922

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab6e9ef6608f'
down_revision = '1671e78f512d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('account', sa.Column('password', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('account', 'password')
    # ### end Alembic commands ###
