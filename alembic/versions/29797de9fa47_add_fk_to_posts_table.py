"""add fk to posts table

Revision ID: 29797de9fa47
Revises: e9bed4e780f5
Create Date: 2022-02-07 15:06:48.936855

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29797de9fa47'
down_revision = 'e9bed4e780f5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts",
                  sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("post_users_fk",
                          source_table="posts",
                          referent_table="users",
                          local_cols=["owner_id"],
                          remote_cols=["id"],
                          ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
