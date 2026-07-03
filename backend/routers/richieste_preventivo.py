# backend/routers/richieste_preventivo.py
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.core.email import send_richiesta_preventivo_email
from backend.core.security import get_current_user, require_role
from backend.crud import condominio as crud_condominio
from backend.crud import richiesta_preventivo as crud_richiesta
from backend.crud import servizio as crud_servizio
from backend.models.user import User, UserRole
from backend.schemas.richiesta_preventivo import RichiestaPreventivoCreate, RichiestaPreventivoOut

router = APIRouter()


@router.post("", response_model=RichiestaPreventivoOut, status_code=status.HTTP_201_CREATED)
def create_richiesta(
    payload: RichiestaPreventivoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
):
    servizio = crud_servizio.get_servizio(db, payload.servizio_id)
    if not servizio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Servizio non trovato")

    condominio = crud_condominio.get_condominio(db, payload.condominio_id)
    if not condominio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Condominio non trovato")
    if condominio.admin_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Non sei l'amministratore di questo condominio")

    richiesta = crud_richiesta.create_richiesta(db, payload, current_user.id)

    for fornitore in servizio.fornitori:
        send_richiesta_preventivo_email(
            to_email=fornitore.email,
            fornitore_nome=fornitore.full_name or fornitore.email,
            admin_nome=current_user.full_name or current_user.email,
            servizio_nome=servizio.nome,
            condominio_denominazione=condominio.denominazione,
            condominio_indirizzo=condominio.indirizzo,
            descrizione=richiesta.descrizione,
        )

    return richiesta


@router.get("", response_model=list[RichiestaPreventivoOut])
def list_richieste(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == UserRole.ADMIN:
        return crud_richiesta.list_richieste_by_admin(db, current_user.id)
    if current_user.role == UserRole.FORNITORE:
        return crud_richiesta.list_richieste_by_fornitore(db, current_user)
    return []
