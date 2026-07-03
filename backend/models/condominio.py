# backend/models/condominio.py
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship

from backend.core.database import Base

condominio_condomino = Table(
    "condominio_condomino",
    Base.metadata,
    Column("condominio_id", Integer, ForeignKey("condomini.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
)


class Condominio(Base):
    """
    Un condominio ha un solo amministratore (FK diretta). I condomini
    (ruolo `condomino`) sono associati in N:M tramite `condominio_condomino`;
    il dettaglio di unità immobiliare/millesimi arriverà in un secondo momento.
    """
    __tablename__ = "condomini"

    id             = Column(Integer, primary_key=True, index=True)
    denominazione  = Column(String(255), nullable=False)
    codice_fiscale = Column(String(16), nullable=False, index=True)
    indirizzo      = Column(String(255), nullable=False)
    admin_id       = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at     = Column(DateTime, default=datetime.utcnow, nullable=False)

    admin = relationship("User", foreign_keys=[admin_id], back_populates="condomini_amministrati")
    condomini = relationship("User", secondary=condominio_condomino, back_populates="condomini_associati")
