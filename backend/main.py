# backend/main.py
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.core.config import settings
from backend.routers import auth, condomini, servizi, fornitori, richieste_preventivo

app = FastAPI(
    title="PortaleFornitoriCondomini API",
    description="API per il portale di gestione fornitori e condomini",
    version="0.1.0",
)

# ── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ──────────────────────────────────────────────────────────────────
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(condomini.router, prefix="/api/condomini", tags=["condomini"])
app.include_router(servizi.router, prefix="/api/servizi", tags=["servizi"])
app.include_router(fornitori.router, prefix="/api/fornitori", tags=["fornitori"])
app.include_router(richieste_preventivo.router, prefix="/api/richieste-preventivo", tags=["richieste-preventivo"])


@app.get("/api/health")
def health_check():
    return {"status": "ok", "version": "0.1.0"}