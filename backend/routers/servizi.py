# backend/routers/servizi.py
from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.core.security import require_role
from backend.crud import servizio as crud_servizio
from backend.models.user import User, UserRole
from backend.schemas.servizio import ServizioCreate, ServizioOut, ServizioPublicOut

router = APIRouter()


@router.get("/public", response_model=list[ServizioPublicOut])
def list_servizi_public(db: Session = Depends(get_db)):
    """Lista non autenticata, usata dal form di registrazione fornitore."""
    return crud_servizio.list_servizi(db)


@router.get("", response_model=list[ServizioOut])
def list_servizi(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
):
    return crud_servizio.list_servizi(db)


@router.post("", response_model=ServizioOut, status_code=status.HTTP_201_CREATED)
def create_servizio(
    payload: ServizioCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
):
    return crud_servizio.create_servizio(db, payload, current_user.id)
