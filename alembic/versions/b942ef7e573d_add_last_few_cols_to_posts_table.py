"""add last few cols to posts table

Revision ID: b942ef7e573d
Revises: 29797de9fa47
Create Date: 2022-02-07 15:12:31.287368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b942ef7e573d'
down_revision = '29797de9fa47'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column(
        "published", sa.Boolean(), nullable=False, server_default="TRUE"
    ))
    op.add_column("posts", sa.Column(
        "created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")
    ))
    pass


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
