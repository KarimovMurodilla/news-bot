"""

Revision ID: 7ca2d80b7580
Revises: 55eda3c444b6
Create Date: 2024-06-11 13:54:05.495572

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ca2d80b7580'
down_revision = '55eda3c444b6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('category', sa.Column('url_id', sa.Integer(), nullable=False))
    op.create_foreign_key(op.f('fk_category_url_id_url'), 'category', 'url', ['url_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('fk_url_category_id_category', 'url', type_='foreignkey')
    op.drop_column('url', 'category_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('url', sa.Column('category_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('fk_url_category_id_category', 'url', 'category', ['category_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(op.f('fk_category_url_id_url'), 'category', type_='foreignkey')
    op.drop_column('category', 'url_id')
    # ### end Alembic commands ###
