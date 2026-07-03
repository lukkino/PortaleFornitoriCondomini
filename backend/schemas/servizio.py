# backend/schemas/servizio.py
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, field_validator


class ServizioBase(BaseModel):
    nome: str
    descrizione: str | None = None

    @field_validator("nome")
    @classmethod
    def _not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Campo obbligatorio")
        return v


class ServizioCreate(ServizioBase):
    pass


class ServizioOut(ServizioBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class ServizioPublicOut(BaseModel):
    """Vista minimale esposta senza autenticazione, per la selezione in fase di registrazione fornitore."""
    id: int
    nome: str
    descrizione: str | None = None

    model_config = {"from_attributes": True}
