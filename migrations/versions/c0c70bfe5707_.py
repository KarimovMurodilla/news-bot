"""

Revision ID: c0c70bfe5707
Revises: 1d700b1a6d54
Create Date: 2024-06-11 14:31:36.403563

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0c70bfe5707'
down_revision = '1d700b1a6d54'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_category_url_id_url', 'category', type_='foreignkey')
    op.drop_column('category', 'url_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('category', sa.Column('url_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('fk_category_url_id_url', 'category', 'url', ['url_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###
