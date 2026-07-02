from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url

from alembic import context

# Carica .env prima di tutto (cerca backend/.env)
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Importa Base e tutti i modelli, cosi' Alembic vede i metadata
# per l'autogenerate.
from backend.core.database import Base
from backend.models import user  # noqa: F401  (registra i modelli su Base)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    import os

    url = os.environ.get("DATABASE_URL") or config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    import os

    raw_url = os.environ.get("DATABASE_URL") or config.get_main_option("sqlalchemy.url")

    # make_url gestisce correttamente i caratteri speciali nella password
    url = make_url(raw_url)

    connectable = create_engine(url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()