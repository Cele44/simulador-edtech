"""
models/estudiante.py — Modelo ORM para la tabla 'estudiantes'
Simulador de Laboratorio Virtual - EdTech
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship          # ← línea nueva
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from database import Base


class Estudiante(Base):
    __tablename__ = "estudiantes"

    id              = Column(Integer, primary_key=True, index=True)
    username        = Column(String(50), unique=True, nullable=False, index=True)
    password_hash   = Column(String(255), nullable=False)
    nombre_completo = Column(String(100))
    email           = Column(String(100))
    rol             = Column(Enum("estudiante", "admin"), default="estudiante")
    activo          = Column(Boolean, default=True)
    fecha_registro  = Column(DateTime, server_default=func.now())
    interacciones   = relationship("InteraccionLab", back_populates="estudiante")  # ← línea nueva