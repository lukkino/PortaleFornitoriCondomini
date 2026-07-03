"""servizi, servizio_fornitore, richieste_preventivo

Revision ID: 0004
Revises: 0003
Create Date: 2026-07-03

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "servizi",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nome", sa.String(length=150), nullable=False),
        sa.Column("descrizione", sa.Text(), nullable=True),
        sa.Column("creato_da_admin_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_servizi_id", "servizi", ["id"])

    op.create_table(
        "servizio_fornitore",
        sa.Column("servizio_id", sa.Integer(), sa.ForeignKey("servizi.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    )

    op.create_table(
        "richieste_preventivo",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("servizio_id", sa.Integer(), sa.ForeignKey("servizi.id", ondelete="CASCADE"), nullable=False),
        sa.Column("condominio_id", sa.Integer(), sa.ForeignKey("condomini.id", ondelete="CASCADE"), nullable=False),
        sa.Column("admin_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("descrizione", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_richieste_preventivo_id", "richieste_preventivo", ["id"])
    op.create_index("ix_richieste_preventivo_servizio_id", "richieste_preventivo", ["servizio_id"])
    op.create_index("ix_richieste_preventivo_condominio_id", "richieste_preventivo", ["condominio_id"])
    op.create_index("ix_richieste_preventivo_admin_id", "richieste_preventivo", ["admin_id"])


def downgrade() -> None:
    op.drop_table("richieste_preventivo")
    op.drop_table("servizio_fornitore")
    op.drop_index("ix_servizi_id", table_name="servizi")
    op.drop_table("servizi")
