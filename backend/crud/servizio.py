# backend/crud/servizio.py
from __future__ import annotations

from sqlalchemy.orm import Session

from backend.models.servizio import Servizio
from backend.models.user import User
from backend.schemas.servizio import ServizioCreate


def create_servizio(db: Session, payload: ServizioCreate, creato_da_admin_id: int) -> Servizio:
    servizio = Servizio(
        nome=payload.nome,
        descrizione=payload.descrizione,
        creato_da_admin_id=creato_da_admin_id,
    )
    db.add(servizio)
    db.commit()
    db.refresh(servizio)
    return servizio


def get_servizio(db: Session, servizio_id: int) -> Servizio | None:
    return db.query(Servizio).filter(Servizio.id == servizio_id).first()


def list_servizi(db: Session) -> list[Servizio]:
    return db.query(Servizio).order_by(Servizio.nome).all()


def get_servizi_by_ids(db: Session, servizio_ids: list[int]) -> list[Servizio]:
    return db.query(Servizio).filter(Servizio.id.in_(servizio_ids)).all()


def add_fornitore(db: Session, servizio: Servizio, user: User) -> None:
    if user not in servizio.fornitori:
        servizio.fornitori.append(user)
        db.commit()
