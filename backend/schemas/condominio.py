# backend/schemas/condominio.py
from __future__ import annotations

import re
from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator

CODICE_FISCALE_RE = re.compile(r"^[0-9A-Za-z]{11,16}$")


class CondominioBase(BaseModel):
    denominazione: str
    codice_fiscale: str
    indirizzo: str

    @field_validator("codice_fiscale")
    @classmethod
    def _validate_codice_fiscale(cls, v: str) -> str:
        v = v.strip().upper()
        if not CODICE_FISCALE_RE.match(v):
            raise ValueError("Codice fiscale non valido (atteso 11-16 caratteri alfanumerici)")
        return v

    @field_validator("denominazione", "indirizzo")
    @classmethod
    def _not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Campo obbligatorio")
        return v


class CondominioCreate(CondominioBase):
    pass


class CondominioUpdate(BaseModel):
    denominazione: str | None = None
    codice_fiscale: str | None = None
    indirizzo: str | None = None


class CondominioOut(CondominioBase):
    id: int
    admin_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class MembroAddRequest(BaseModel):
    email: EmailStr


class CondominioPublicOut(BaseModel):
    """Vista minimale esposta senza autenticazione, per la selezione in fase di registrazione."""
    id: int
    denominazione: str
    indirizzo: str

    model_config = {"from_attributes": True}
