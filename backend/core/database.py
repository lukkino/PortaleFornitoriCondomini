# backend/core/database.py
from __future__ import annotations

from pathlib import Path
from dotenv import load_dotenv

# Carica .env dalla cartella backend/
load_dotenv(Path(__file__).parent.parent / ".env")

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from backend.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,   # verifica connessione prima di usarla
    pool_size=5,
    max_overflow=10,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Dependency FastAPI per ottenere una sessione DB.
    Usare con Depends(get_db) negli endpoint.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()