# backend/routers/auth.py
from __future__ import annotations

import re

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.core.security import verify_password, create_access_token, get_current_user
from backend.crud import condominio as crud_condominio
from backend.crud import servizio as crud_servizio
from backend.crud import user as crud_user
from backend.models.user import User, UserRole
from backend.schemas.user import UserCreate, UserOut, TokenOut, RefreshRequest, AccessTokenOut

router = APIRouter()


# ── Validazione password ──────────────────────────────────────────────────────

def _validate_password(password: str) -> None:
    errors = []
    if len(password) < 8:
        errors.append("almeno 8 caratteri")
    if not re.search(r"[A-Z]", password):
        errors.append("almeno una lettera maiuscola")
    if not re.search(r"[a-z]", password):
        errors.append("almeno una lettera minuscola")
    if not re.search(r"[0-9]", password):
        errors.append("almeno un numero")
    if errors:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Password non sufficientemente robusta. Manca: {', '.join(errors)}.",
        )


# ── POST /api/auth/register ───────────────────────────────────────────────────

@router.post("/register", response_model=TokenOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    _validate_password(payload.password)

    if crud_user.get_user_by_email(db, payload.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email già registrata")

    condominio = None
    if payload.role == UserRole.CONDOMINO:
        condominio = crud_condominio.get_condominio(db, payload.condominio_id)
        if not condominio:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Condominio non trovato")

    servizi = []
    if payload.role == UserRole.FORNITORE:
        servizi = crud_servizio.get_servizi_by_ids(db, payload.servizio_ids)
        if len(servizi) != len(set(payload.servizio_ids)):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Uno o più servizi selezionati non esistono")

    user = crud_user.create_user(db, payload)
    if condominio:
        crud_condominio.add_membro(db, condominio, user)
    for servizio in servizi:
        crud_servizio.add_fornitore(db, servizio, user)

    access_token = create_access_token(user.id)
    refresh_token = crud_user.create_refresh_token(db, user.id)

    return TokenOut(access_token=access_token, refresh_token=refresh_token, user=UserOut.model_validate(user))


# ── POST /api/auth/login ──────────────────────────────────────────────────────

@router.post("/login", response_model=TokenOut)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db, form.username)
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenziali non valide",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account disattivato")

    access_token = create_access_token(user.id)
    refresh_token = crud_user.create_refresh_token(db, user.id)

    return TokenOut(access_token=access_token, refresh_token=refresh_token, user=UserOut.model_validate(user))


# ── POST /api/auth/refresh ────────────────────────────────────────────────────

@router.post("/refresh", response_model=AccessTokenOut)
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)):
    rt = crud_user.get_valid_refresh_token(db, payload.refresh_token)
    if not rt:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token non valido o scaduto")

    # Rotazione: revoca il vecchio refresh token ed emette uno nuovo
    crud_user.revoke_refresh_token(db, rt)
    new_refresh_token = crud_user.create_refresh_token(db, rt.user_id)
    new_access_token = create_access_token(rt.user_id)

    return AccessTokenOut(access_token=new_access_token, refresh_token=new_refresh_token)


# ── POST /api/auth/logout ─────────────────────────────────────────────────────

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(payload: RefreshRequest, db: Session = Depends(get_db)):
    rt = crud_user.get_valid_refresh_token(db, payload.refresh_token)
    if rt:
        crud_user.revoke_refresh_token(db, rt)


# ── GET /api/auth/me ──────────────────────────────────────────────────────────

@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user