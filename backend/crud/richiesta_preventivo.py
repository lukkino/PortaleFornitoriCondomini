# backend/crud/richiesta_preventivo.py
from __future__ import annotations

from sqlalchemy.orm import Session

from backend.models.richiesta_preventivo import RichiestaPreventivo
from backend.models.user import User
from backend.schemas.richiesta_preventivo import RichiestaPreventivoCreate


def create_richiesta(db: Session, payload: RichiestaPreventivoCreate, admin_id: int) -> RichiestaPreventivo:
    richiesta = RichiestaPreventivo(
        servizio_id=payload.servizio_id,
        condominio_id=payload.condominio_id,
        admin_id=admin_id,
        descrizione=payload.descrizione,
    )
    db.add(richiesta)
    db.commit()
    db.refresh(richiesta)
    return richiesta


def list_richieste_by_admin(db: Session, admin_id: int) -> list[RichiestaPreventivo]:
    return (
        db.query(RichiestaPreventivo)
        .filter(RichiestaPreventivo.admin_id == admin_id)
        .order_by(RichiestaPreventivo.created_at.desc())
        .all()
    )


def list_richieste_by_fornitore(db: Session, fornitore: User) -> list[RichiestaPreventivo]:
    servizio_ids = [s.id for s in fornitore.servizi_offerti]
    if not servizio_ids:
        return []
    return (
        db.query(RichiestaPreventivo)
        .filter(RichiestaPreventivo.servizio_id.in_(servizio_ids))
        .order_by(RichiestaPreventivo.created_at.desc())
        .all()
    )
