"""
main.py — Punto de entrada del backend FastAPI
Simulador de Laboratorio Virtual - EdTech
Autor: Ortiz Cadena Maria Celeste Camila

Ejecutar con:
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from app.routers import auth, labs

# ── Crear tablas en la BD si no existen ──────────────────
# (En producción usa Alembic para migraciones)
from app.models import estudiante, interaccion  # noqa: F401 — necesario para que Base las registre
Base.metadata.create_all(bind=engine)

# ── Aplicación FastAPI ────────────────────────────────────
app = FastAPI(
    title="Laboratorio Virtual API",
    description="Backend para el simulador de laboratorio virtual EdTech",
    version="1.0.0",
)

# ── CORS: permite que el frontend (Pygame / cualquier cliente) se conecte ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # En producción especifica el origen exacto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Registrar routers ─────────────────────────────────────
app.include_router(auth.router)
app.include_router(labs.router)


@app.get("/")
def raiz():
    return {"mensaje": "Laboratorio Virtual API funcionando ✓"}


@app.get("/salud")
def salud():
    return {"estado": "ok"}


if __name__ == "__main__":
    import uvicorn
    from config import API_HOST, API_PORT
    uvicorn.run("main:app", host=API_HOST, port=API_PORT, reload=True)
