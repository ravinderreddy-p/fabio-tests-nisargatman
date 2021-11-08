"""Fixed Cascade Delete for all the models

Revision ID: 5dd60edf86c7
Revises: af93cfe21e07
Create Date: 2021-11-08 11:09:03.118551

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5dd60edf86c7'
down_revision = 'af93cfe21e07'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('cities_country_id_fkey', 'cities', type_='foreignkey')
    op.create_foreign_key(None, 'cities', 'countries', ['country_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'cities', type_='foreignkey')
    op.create_foreign_key('cities_country_id_fkey', 'cities', 'countries', ['country_id'], ['id'])
    # ### end Alembic commands ###