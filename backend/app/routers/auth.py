"""
routers/auth.py — Endpoints de autenticación: login y registro de estudiantes.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from database import get_db
from app.schemas.usuario import LoginRequest, TokenResponse, EstudianteCreate, EstudianteOut
from app.repositories import estudiante_repo
from app.services.auth_service import verificar_password, crear_token

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=TokenResponse)
def login(datos: LoginRequest, db: Session = Depends(get_db)):
    """
    Verifica usuario y contraseña contra la BD.
    Si son correctos, devuelve un token JWT para las siguientes peticiones.
    """
    estudiante = estudiante_repo.obtener_por_username(db, datos.username)

    if not estudiante or not verificar_password(datos.password, estudiante.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
        )
    if not estudiante.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cuenta desactivada",
        )

    token = crear_token({
        "sub": str(estudiante.id),
        "username": estudiante.username,
        "rol": estudiante.rol,
    })

    return TokenResponse(
        access_token = token,
        username     = estudiante.username,
        rol          = estudiante.rol,
    )


@router.post("/registro", response_model=EstudianteOut, status_code=201)
def registrar(datos: EstudianteCreate, db: Session = Depends(get_db)):
    """Crea un nuevo estudiante en la BD."""
    existente = estudiante_repo.obtener_por_username(db, datos.username)
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está en uso",
        )
    return estudiante_repo.crear_estudiante(db, datos)


@router.get("/estudiantes", response_model=list[EstudianteOut])
def listar(db: Session = Depends(get_db)):
    """Lista todos los estudiantes (solo para admin, en producción agrega seguridad)."""
    return estudiante_repo.listar_estudiantes(db)
