"""
repositories/estudiante_repo.py — Acceso a datos: operaciones CRUD de estudiantes.
Separa la lógica de BD de los routers.
"""

from sqlalchemy.orm import Session
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from app.models.estudiante import Estudiante
from app.models.interaccion import InteraccionLab
from app.schemas.usuario import EstudianteCreate
from app.services.auth_service import hashear_password
from datetime import datetime


def obtener_por_username(db: Session, username: str) -> Estudiante | None:
    return db.query(Estudiante).filter(Estudiante.username == username).first()


def obtener_por_id(db: Session, estudiante_id: int) -> Estudiante | None:
    return db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()


def listar_estudiantes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Estudiante).offset(skip).limit(limit).all()


def crear_estudiante(db: Session, datos: EstudianteCreate) -> Estudiante:
    estudiante = Estudiante(
        username        = datos.username,
        password_hash   = hashear_password(datos.password),
        nombre_completo = datos.nombre_completo,
        email           = datos.email,
        rol             = datos.rol,
    )
    db.add(estudiante)
    db.commit()
    db.refresh(estudiante)
    return estudiante


# ── Interacciones con laboratorios ────────────────────────

def iniciar_interaccion(db: Session, estudiante_id: int, laboratorio: str) -> InteraccionLab:
    interaccion = InteraccionLab(
        estudiante_id = estudiante_id,
        laboratorio   = laboratorio,
    )
    db.add(interaccion)
    db.commit()
    db.refresh(interaccion)
    return interaccion


def finalizar_interaccion(
    db: Session,
    interaccion_id: int,
    duracion_segundos: int,
    completo: bool,
) -> InteraccionLab | None:
    interaccion = db.query(InteraccionLab).filter(
        InteraccionLab.id == interaccion_id
    ).first()
    if not interaccion:
        return None
    interaccion.fecha_fin          = datetime.utcnow()
    interaccion.duracion_segundos  = duracion_segundos
    interaccion.completo           = completo
    db.commit()
    db.refresh(interaccion)
    return interaccion


def historial_estudiante(db: Session, estudiante_id: int):
    return db.query(InteraccionLab).filter(
        InteraccionLab.estudiante_id == estudiante_id
    ).order_by(InteraccionLab.fecha_inicio.desc()).all()
