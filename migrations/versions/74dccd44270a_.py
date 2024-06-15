"""

Revision ID: 74dccd44270a
Revises: 5d74702bad08
Create Date: 2024-06-10 15:40:08.880704

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '74dccd44270a'
down_revision = '5d74702bad08'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('news', sa.Column('language', sa.VARCHAR(length=50), nullable=True))
    op.add_column('source', sa.Column('language', sa.VARCHAR(length=50), nullable=True))
    op.create_unique_constraint(op.f('uq_source_url'), 'source', ['url'])
    op.add_column('user', sa.Column('language', sa.VARCHAR(length=50), nullable=True))
    op.drop_column('user', 'language_code')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('language_code', postgresql.ENUM('EN', 'RU', 'UZ', name='locales'), autoincrement=False, nullable=True))
    op.drop_column('user', 'language')
    op.drop_constraint(op.f('uq_source_url'), 'source', type_='unique')
    op.drop_column('source', 'language')
    op.drop_column('news', 'language')
    # ### end Alembic commands ###
