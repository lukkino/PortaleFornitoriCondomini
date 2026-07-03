# backend/routers/condomini.py
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.core.security import get_current_user, require_role
from backend.crud import condominio as crud_condominio
from backend.crud import user as crud_user
from backend.models.condominio import Condominio
from backend.models.user import User, UserRole
from backend.schemas.condominio import (
    CondominioCreate,
    CondominioUpdate,
    CondominioOut,
    CondominioPublicOut,
    MembroAddRequest,
)
from backend.schemas.user import UserOut

router = APIRouter()


def _get_owned_condominio(db: Session, condominio_id: int, current_user: User) -> Condominio:
    condominio = crud_condominio.get_condominio(db, condominio_id)
    if not condominio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Condominio non trovato")
    if condominio.admin_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Non sei l'amministratore di questo condominio")
    return condominio


@router.post("", response_model=CondominioOut, status_code=status.HTTP_201_CREATED)
def create_condominio(
    payload: CondominioCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
):
    return crud_condominio.create_condominio(db, payload, current_user.id)


@router.get("/public", response_model=list[CondominioPublicOut])
def list_condomini_public(db: Session = Depends(get_db)):
    """Lista non autenticata (solo denominazione/indirizzo), usata dal form di registrazione condomino."""
    return crud_condominio.list_condomini_public(db)


@router.get("", response_model=list[CondominioOut])
def list_condomini(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == UserRole.ADMIN:
        return crud_condominio.list_condomini_by_admin(db, current_user.id)
    if current_user.role == UserRole.CONDOMINO:
        return crud_condominio.list_condomini_by_condomino(db, current_user)
    return []


@router.get("/{condominio_id}", response_model=CondominioOut)
def get_condominio(
    condominio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    condominio = crud_condominio.get_condominio(db, condominio_id)
    if not condominio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Condominio non trovato")
    is_owner = condominio.admin_id == current_user.id
    is_member = any(u.id == current_user.id for u in condominio.condomini)
    if not (is_owner or is_member):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Non hai accesso a questo condominio")
    return condominio


@router.put("/{condominio_id}", response_model=CondominioOut)
def update_condominio(
    condominio_id: int,
    payload: CondominioUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
):
    condominio = _get_owned_condominio(db, condominio_id, current_user)
    return crud_condominio.update_condominio(db, condominio, payload)


@router.delete("/{condominio_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_condominio(
    condominio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
):
    condominio = _get_owned_condominio(db, condominio_id, current_user)
    crud_condominio.delete_condominio(db, condominio)


@router.get("/{condominio_id}/membri", response_model=list[UserOut])
def list_membri(
    condominio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
):
    condominio = _get_owned_condominio(db, condominio_id, current_user)
    return condominio.condomini


@router.post("/{condominio_id}/membri", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def add_membro(
    condominio_id: int,
    payload: MembroAddRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
):
    condominio = _get_owned_condominio(db, condominio_id, current_user)
    user = crud_user.get_user_by_email(db, payload.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nessun utente trovato con questa email")
    if user.role != UserRole.CONDOMINO:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="L'utente non ha ruolo Condomino")
    crud_condominio.add_membro(db, condominio, user)
    return user


@router.delete("/{condominio_id}/membri/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_membro(
    condominio_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
):
    condominio = _get_owned_condominio(db, condominio_id, current_user)
    target = next((u for u in condominio.condomini if u.id == user_id), None)
    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utente non associato a questo condominio")
    crud_condominio.remove_membro(db, condominio, target)
