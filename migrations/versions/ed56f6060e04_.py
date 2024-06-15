"""

Revision ID: ed56f6060e04
Revises: 74dccd44270a
Create Date: 2024-06-11 11:06:42.529628

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed56f6060e04'
down_revision = '74dccd44270a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('url',
    sa.Column('url', sa.Text(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('source_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], name=op.f('fk_url_category_id_category'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['source_id'], ['source.id'], name=op.f('fk_url_source_id_source'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_url')),
    sa.UniqueConstraint('url', name=op.f('uq_url_url'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('url')
    # ### end Alembic commands ###
