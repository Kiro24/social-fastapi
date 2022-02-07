"""add user table

Revision ID: e9bed4e780f5
Revises: 956a3eccc4cb
Create Date: 2022-02-07 14:59:26.482346

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9bed4e780f5'
down_revision = '956a3eccc4cb'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users",
                    sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email"),
                    )
    pass


def downgrade():
    op.drop_table("users")
    pass
