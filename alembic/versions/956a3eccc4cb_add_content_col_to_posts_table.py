"""add content col to posts table

Revision ID: 956a3eccc4cb
Revises: 0d5a47757d9c
Create Date: 2022-02-07 14:54:54.465739

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '956a3eccc4cb'
down_revision = '0d5a47757d9c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts",
                  sa.Column("content", sa.String(), nullable=False)
                  )
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
