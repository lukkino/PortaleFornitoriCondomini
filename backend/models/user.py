# backend/models/user.py
from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import relationship

from backend.core.database import Base


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    CONDOMINO = "condomino"
    FORNITORE = "fornitore"


class User(Base):
    """
    Utente del portale. Il campo `role` distingue le 3 tipologie
    (Amministratori, Condomini, Fornitori). Ogni utente vede solo
    i propri dati: le tabelle future dovranno referenziare user_id.
    """
    __tablename__ = "users"

    id              = Column(Integer, primary_key=True, index=True)
    email           = Column(String(255), unique=True, index=True, nullable=False)
    full_name       = Column(String(150), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    role            = Column(SAEnum(UserRole, name="user_role"), nullable=False, default=UserRole.CONDOMINO)
    is_active       = Column(Boolean, default=True, nullable=False)
    created_at      = Column(DateTime, default=datetime.utcnow, nullable=False)

    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")


class RefreshToken(Base):
    """
    Refresh token opachi (non JWT) salvati in DB per poterli revocare
    singolarmente al logout o in caso di rotazione.
    """
    __tablename__ = "refresh_tokens"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token      = Column(String(255), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    revoked    = Column(Boolean, default=False, nullable=False)

    user = relationship("User", back_populates="refresh_tokens")