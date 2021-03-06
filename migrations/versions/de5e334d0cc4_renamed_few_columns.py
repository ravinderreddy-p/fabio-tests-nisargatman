"""renamed few columns

Revision ID: de5e334d0cc4
Revises: 3d577430ccff
Create Date: 2021-11-07 11:51:09.512125

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de5e334d0cc4'
down_revision = '3d577430ccff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cities', sa.Column('number_of_roads', sa.Integer(), nullable=True))
    op.add_column('cities', sa.Column('number_of_trees', sa.Integer(), nullable=True))
    op.drop_column('cities', 'trees_count')
    op.drop_column('cities', 'roads_count')
    op.add_column('countries', sa.Column('number_of_hospitals', sa.Integer(), nullable=True))
    op.add_column('countries', sa.Column('number_of_national_parks', sa.Integer(), nullable=True))
    op.drop_column('countries', 'national_parks_count')
    op.drop_column('countries', 'hospitals_count')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('countries', sa.Column('hospitals_count', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('countries', sa.Column('national_parks_count', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('countries', 'number_of_national_parks')
    op.drop_column('countries', 'number_of_hospitals')
    op.add_column('cities', sa.Column('roads_count', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('cities', sa.Column('trees_count', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('cities', 'number_of_trees')
    op.drop_column('cities', 'number_of_roads')
    # ### end Alembic commands ###
