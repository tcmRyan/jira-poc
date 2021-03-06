"""empty message

Revision ID: a3ff2c87adc5
Revises: 
Create Date: 2017-08-11 08:40:19.764050

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3ff2c87adc5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authentications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('key', sa.String(), nullable=True),
    sa.Column('client_key', sa.String(), nullable=True),
    sa.Column('shared_secret', sa.String(), nullable=True),
    sa.Column('plugins_version', sa.String(), nullable=True),
    sa.Column('base_url', sa.String(), nullable=True),
    sa.Column('product_type', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('service_entitlement_number', sa.String(), nullable=True),
    sa.Column('event_type', sa.String(), nullable=True),
    sa.Column('oauth_client_id', sa.String(), nullable=True),
    sa.Column('installed_by', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('authentications')
    # ### end Alembic commands ###
