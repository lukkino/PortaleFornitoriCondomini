# backend/schemas/fornitore.py
from __future__ import annotations

from pydantic import BaseModel, EmailStr

from backend.schemas.servizio import ServizioOut


class FornitoreOut(BaseModel):
    id: int
    full_name: str | None = None
    email: EmailStr
    servizi_offerti: list[ServizioOut] = []

    model_config = {"from_attributes": True}
