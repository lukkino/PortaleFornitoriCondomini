"""scheda anagrafica condomino su users

Revision ID: 0003
Revises: 0002
Create Date: 2026-07-03

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("nome", sa.String(length=100), nullable=True))
    op.add_column("users", sa.Column("cognome", sa.String(length=100), nullable=True))
    op.add_column("users", sa.Column("codice_fiscale", sa.String(length=16), nullable=True))
    op.add_column("users", sa.Column("telefono", sa.String(length=30), nullable=True))
    op.add_column("users", sa.Column("pec", sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "pec")
    op.drop_column("users", "telefono")
    op.drop_column("users", "codice_fiscale")
    op.drop_column("users", "cognome")
    op.drop_column("users", "nome")
