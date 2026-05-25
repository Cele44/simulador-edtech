"""
schemas/interaccion.py — Schemas para registrar interacciones con laboratorios.
"""

from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime


class IniciarLabRequest(BaseModel):
    """El frontend manda esto cuando el estudiante entra a un lab."""
    laboratorio: Literal["quimica", "fisica"]


class FinalizarLabRequest(BaseModel):
    """El frontend manda esto cuando el estudiante termina o sale del lab."""
    interaccion_id: int
    duracion_segundos: int
    completo: bool = False


class InteraccionOut(BaseModel):
    """Respuesta al registrar una interacción."""
    id: int
    estudiante_id: int
    laboratorio: str
    fecha_inicio: datetime
    fecha_fin: Optional[datetime] = None
    duracion_segundos: Optional[int] = None
    completo: bool

    class Config:
        from_attributes = True
