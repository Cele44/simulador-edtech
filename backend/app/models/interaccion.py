"""
models/interaccion.py — Modelo ORM para la tabla 'interacciones_lab'
Registra cada sesión de un estudiante en un laboratorio.
"""

from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from database import Base


class InteraccionLab(Base):
    __tablename__ = "interacciones_lab"

    id                 = Column(Integer, primary_key=True, index=True)
    estudiante_id      = Column(Integer, ForeignKey("estudiantes.id"), nullable=False)
    laboratorio        = Column(Enum("quimica", "fisica"), nullable=False)
    fecha_inicio       = Column(DateTime, server_default=func.now())
    fecha_fin          = Column(DateTime, nullable=True)
    duracion_segundos  = Column(Integer, nullable=True)
    completo           = Column(Boolean, default=False)

    # Relación para acceder al estudiante desde una interacción
    estudiante = relationship("Estudiante", back_populates="interacciones")
