# backend/models/richiesta_preventivo.py
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from backend.core.database import Base


class RichiestaPreventivo(Base):
    """Richiesta di preventivo creata da un admin per un servizio, relativa a un suo condominio."""
    __tablename__ = "richieste_preventivo"

    id             = Column(Integer, primary_key=True, index=True)
    servizio_id    = Column(Integer, ForeignKey("servizi.id", ondelete="CASCADE"), nullable=False, index=True)
    condominio_id  = Column(Integer, ForeignKey("condomini.id", ondelete="CASCADE"), nullable=False, index=True)
    admin_id       = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    descrizione    = Column(Text, nullable=True)
    created_at     = Column(DateTime, default=datetime.utcnow, nullable=False)

    servizio   = relationship("Servizio")
    condominio = relationship("Condominio")
    admin      = relationship("User")
