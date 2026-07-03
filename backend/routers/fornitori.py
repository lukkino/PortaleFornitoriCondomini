# backend/routers/fornitori.py
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.core.security import require_role
from backend.crud import user as crud_user
from backend.models.user import User, UserRole
from backend.schemas.fornitore import FornitoreOut

router = APIRouter()


@router.get("", response_model=list[FornitoreOut])
def list_fornitori(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
):
    return crud_user.list_fornitori(db)
