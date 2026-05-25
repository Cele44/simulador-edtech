"""
routers/labs.py — Endpoints para registrar interacciones con laboratorios.
El frontend llama estos endpoints al entrar/salir de un laboratorio.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from database import get_db
from app.schemas.interaccion import IniciarLabRequest, FinalizarLabRequest, InteraccionOut
from app.repositories import estudiante_repo
from app.services.auth_service import verificar_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/labs", tags=["Laboratorios"])
security = HTTPBearer()


def obtener_estudiante_actual(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """Extrae el estudiante del token JWT en cada petición protegida."""
    payload = verificar_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    estudiante_id = int(payload.get("sub"))
    estudiante = estudiante_repo.obtener_por_id(db, estudiante_id)
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return estudiante


@router.post("/iniciar", response_model=InteraccionOut)
def iniciar_lab(
    datos: IniciarLabRequest,
    db: Session = Depends(get_db),
    estudiante=Depends(obtener_estudiante_actual),
):
    """
    Registra el momento en que un estudiante entra a un laboratorio.
    El frontend llama esto cuando el usuario selecciona un lab del menú.
    """
    interaccion = estudiante_repo.iniciar_interaccion(
        db, estudiante.id, datos.laboratorio
    )
    return interaccion


@router.put("/finalizar", response_model=InteraccionOut)
def finalizar_lab(
    datos: FinalizarLabRequest,
    db: Session = Depends(get_db),
    estudiante=Depends(obtener_estudiante_actual),
):
    """
    Registra el tiempo y si completó el laboratorio.
    El frontend llama esto al presionar VOLVER o cuando se acaba el tiempo.
    """
    interaccion = estudiante_repo.finalizar_interaccion(
        db, datos.interaccion_id, datos.duracion_segundos, datos.completo
    )
    if not interaccion:
        raise HTTPException(status_code=404, detail="Interacción no encontrada")
    return interaccion


@router.get("/historial/{estudiante_id}", response_model=list[InteraccionOut])
def historial(
    estudiante_id: int,
    db: Session = Depends(get_db),
    estudiante=Depends(obtener_estudiante_actual),
):
    """Devuelve el historial de laboratorios de un estudiante."""
    return estudiante_repo.historial_estudiante(db, estudiante_id)
