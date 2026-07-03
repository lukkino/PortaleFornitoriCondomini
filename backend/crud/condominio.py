# backend/crud/condominio.py
from __future__ import annotations

from sqlalchemy.orm import Session

from backend.models.condominio import Condominio
from backend.models.user import User
from backend.schemas.condominio import CondominioCreate, CondominioUpdate


def create_condominio(db: Session, payload: CondominioCreate, admin_id: int) -> Condominio:
    condominio = Condominio(
        denominazione=payload.denominazione,
        codice_fiscale=payload.codice_fiscale,
        indirizzo=payload.indirizzo,
        admin_id=admin_id,
    )
    db.add(condominio)
    db.commit()
    db.refresh(condominio)
    return condominio


def get_condominio(db: Session, condominio_id: int) -> Condominio | None:
    return db.query(Condominio).filter(Condominio.id == condominio_id).first()


def list_condomini_by_admin(db: Session, admin_id: int) -> list[Condominio]:
    return (
        db.query(Condominio)
        .filter(Condominio.admin_id == admin_id)
        .order_by(Condominio.created_at.desc())
        .all()
    )


def list_condomini_by_condomino(db: Session, user: User) -> list[Condominio]:
    return user.condomini_associati


def list_condomini_public(db: Session) -> list[Condominio]:
    return db.query(Condominio).order_by(Condominio.denominazione).all()


def update_condominio(db: Session, condominio: Condominio, payload: CondominioUpdate) -> Condominio:
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(condominio, field, value)
    db.commit()
    db.refresh(condominio)
    return condominio


def delete_condominio(db: Session, condominio: Condominio) -> None:
    db.delete(condominio)
    db.commit()


def add_membro(db: Session, condominio: Condominio, user: User) -> None:
    if user not in condominio.condomini:
        condominio.condomini.append(user)
        db.commit()


def remove_membro(db: Session, condominio: Condominio, user: User) -> None:
    if user in condominio.condomini:
        condominio.condomini.remove(user)
        db.commit()
