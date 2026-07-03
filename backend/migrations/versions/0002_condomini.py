"""condomini + associazione condomino

Revision ID: 0002
Revises: 0001
Create Date: 2026-07-03

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "condomini",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("denominazione", sa.String(length=255), nullable=False),
        sa.Column("codice_fiscale", sa.String(length=16), nullable=False),
        sa.Column("indirizzo", sa.String(length=255), nullable=False),
        sa.Column("admin_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_condomini_id", "condomini", ["id"])
    op.create_index("ix_condomini_codice_fiscale", "condomini", ["codice_fiscale"])
    op.create_index("ix_condomini_admin_id", "condomini", ["admin_id"])

    op.create_table(
        "condominio_condomino",
        sa.Column("condominio_id", sa.Integer(), sa.ForeignKey("condomini.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    )


def downgrade() -> None:
    op.drop_table("condominio_condomino")

    op.drop_index("ix_condomini_admin_id", table_name="condomini")
    op.drop_index("ix_condomini_codice_fiscale", table_name="condomini")
    op.drop_index("ix_condomini_id", table_name="condomini")
    op.drop_table("condomini")
