"""empty message

Revision ID: cace8299986e
Revises: 684845248459
Create Date: 2017-08-27 17:20:08.449892

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cace8299986e'
down_revision = '684845248459'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('authentications', sa.Column('installedBy', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('authentications', 'installedBy')
    # ### end Alembic commands ###