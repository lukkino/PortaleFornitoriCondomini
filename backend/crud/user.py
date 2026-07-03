# backend/crud/user.py
from __future__ import annotations

from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from backend.core.config import settings
from backend.core.security import hash_password, generate_refresh_token
from backend.models.user import User, RefreshToken, UserRole
from backend.schemas.user import UserCreate


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def list_fornitori(db: Session) -> list[User]:
    return db.query(User).filter(User.role == UserRole.FORNITORE).order_by(User.full_name).all()


def create_user(db: Session, payload: UserCreate) -> User:
    full_name = payload.full_name
    if payload.nome and payload.cognome:
        full_name = f"{payload.nome} {payload.cognome}"

    user = User(
        email=payload.email,
        full_name=full_name,
        hashed_password=hash_password(payload.password),
        role=payload.role,
        nome=payload.nome,
        cognome=payload.cognome,
        codice_fiscale=payload.codice_fiscale,
        telefono=payload.telefono,
        pec=payload.pec,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_refresh_token(db: Session, user_id: int) -> str:
    token = generate_refresh_token()
    expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    db.add(RefreshToken(user_id=user_id, token=token, expires_at=expires_at))
    db.commit()
    return token


def get_valid_refresh_token(db: Session, token: str) -> RefreshToken | None:
    rt = db.query(RefreshToken).filter(RefreshToken.token == token).first()
    if not rt or rt.revoked or rt.expires_at < datetime.utcnow():
        return None
    return rt


def revoke_refresh_token(db: Session, rt: RefreshToken) -> None:
    rt.revoked = True
    db.commit()