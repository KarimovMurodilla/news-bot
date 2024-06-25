"""

Revision ID: 024a2a85fbb7
Revises: 3fdcee8882b7
Create Date: 2024-06-25 12:20:04.614642

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '024a2a85fbb7'
down_revision = '3fdcee8882b7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('news', sa.Column('similarity', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('news', 'similarity')
    # ### end Alembic commands ###