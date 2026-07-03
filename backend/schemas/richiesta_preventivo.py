# backend/schemas/richiesta_preventivo.py
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr


class RichiestaPreventivoCreate(BaseModel):
    servizio_id: int
    condominio_id: int
    descrizione: str | None = None


class RichiestaAdminOut(BaseModel):
    full_name: str | None = None
    email: EmailStr

    model_config = {"from_attributes": True}


class RichiestaServizioOut(BaseModel):
    id: int
    nome: str

    model_config = {"from_attributes": True}


class RichiestaCondominioOut(BaseModel):
    id: int
    denominazione: str
    indirizzo: str

    model_config = {"from_attributes": True}


class RichiestaPreventivoOut(BaseModel):
    id: int
    descrizione: str | None
    created_at: datetime
    admin: RichiestaAdminOut
    servizio: RichiestaServizioOut
    condominio: RichiestaCondominioOut

    model_config = {"from_attributes": True}
