"""

Revision ID: d91ebcea7e06
Revises: eecb2cfb7e27
Create Date: 2024-06-25 14:52:01.950209

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd91ebcea7e06'
down_revision = 'eecb2cfb7e27'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uq_similars_similarity', 'similars', type_='unique')
    op.drop_constraint('uq_similars_title1', 'similars', type_='unique')
    op.drop_constraint('uq_similars_title2', 'similars', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('uq_similars_title2', 'similars', ['title2'])
    op.create_unique_constraint('uq_similars_title1', 'similars', ['title1'])
    op.create_unique_constraint('uq_similars_similarity', 'similars', ['similarity'])
    # ### end Alembic commands ###
