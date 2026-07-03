# backend/models/servizio.py
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship

from backend.core.database import Base

servizio_fornitore = Table(
    "servizio_fornitore",
    Base.metadata,
    Column("servizio_id", Integer, ForeignKey("servizi.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
)


class Servizio(Base):
    """
    Catalogo condiviso tra tutti gli amministratori (non di proprietà esclusiva
    di chi lo crea): un fornitore si registra scegliendo tra questi servizi, e
    qualsiasi admin può poi raggiungere i fornitori registrati per un servizio.
    """
    __tablename__ = "servizi"

    id                 = Column(Integer, primary_key=True, index=True)
    nome               = Column(String(150), nullable=False)
    descrizione        = Column(Text, nullable=True)
    creato_da_admin_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at         = Column(DateTime, default=datetime.utcnow, nullable=False)

    fornitori = relationship("User", secondary=servizio_fornitore, back_populates="servizi_offerti")
