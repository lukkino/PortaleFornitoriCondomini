# backend/schemas/user.py
from __future__ import annotations

import re
from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator, model_validator

from backend.models.user import UserRole

PERSONA_CODICE_FISCALE_RE = re.compile(r"^[0-9A-Za-z]{11,16}$")


# ── User ──────────────────────────────────────────────────────────────────────

class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None


class UserCreate(UserBase):
    password: str
    role: UserRole

    # Scheda anagrafica condomino — obbligatori solo quando role == condomino
    nome: str | None = None
    cognome: str | None = None
    codice_fiscale: str | None = None
    telefono: str | None = None
    pec: EmailStr | None = None
    condominio_id: int | None = None

    # Fornitore — obbligatorio solo quando role == fornitore
    servizio_ids: list[int] | None = None

    @field_validator("codice_fiscale")
    @classmethod
    def _validate_codice_fiscale(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.strip().upper()
        if not PERSONA_CODICE_FISCALE_RE.match(v):
            raise ValueError("Codice fiscale non valido (atteso 11-16 caratteri alfanumerici)")
        return v

    @model_validator(mode="after")
    def _validate_condomino_fields(self):
        if self.role == UserRole.CONDOMINO:
            missing = [
                name for name, value in (
                    ("nome", self.nome),
                    ("cognome", self.cognome),
                    ("codice_fiscale", self.codice_fiscale),
                    ("telefono", self.telefono),
                    ("condominio_id", self.condominio_id),
                )
                if not value
            ]
            if missing:
                raise ValueError(f"Campi obbligatori mancanti per il condomino: {', '.join(missing)}")
        if self.role == UserRole.FORNITORE and not self.servizio_ids:
            raise ValueError("Seleziona almeno un servizio offerto")
        return self


class UserOut(UserBase):
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime
    nome: str | None = None
    cognome: str | None = None
    codice_fiscale: str | None = None
    telefono: str | None = None
    pec: str | None = None

    model_config = {"from_attributes": True}


# ── Auth ──────────────────────────────────────────────────────────────────────

class TokenOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserOut


class RefreshRequest(BaseModel):
    refresh_token: str


class AccessTokenOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"