"""
schemas/usuario.py — Schemas Pydantic para validar datos de entrada/salida
No confundir con los modelos SQLAlchemy (esos son para la BD).
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LoginRequest(BaseModel):
    """Lo que manda el frontend al hacer login."""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Lo que devuelve el backend tras login exitoso."""
    access_token: str
    token_type: str = "bearer"
    username: str
    rol: str


class EstudianteBase(BaseModel):
    username: str
    nombre_completo: Optional[str] = None
    email: Optional[str] = None
    rol: str = "estudiante"


class EstudianteCreate(EstudianteBase):
    """Para registrar un nuevo estudiante (incluye contraseña)."""
    password: str


class EstudianteOut(EstudianteBase):
    """Datos del estudiante que devuelve la API (sin contraseña)."""
    id: int
    activo: bool
    fecha_registro: datetime

    class Config:
        from_attributes = True
