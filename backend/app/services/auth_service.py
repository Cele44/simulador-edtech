"""
services/auth_service.py — Lógica de autenticación: hash de contraseñas y JWT.
"""

from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashear_password(password: str) -> str:
    """Convierte la contraseña en texto a un hash seguro."""
    return pwd_context.hash(password)


def verificar_password(password_plano: str, password_hash: str) -> bool:
    """Compara la contraseña ingresada con el hash guardado en la BD."""
    return pwd_context.verify(password_plano, password_hash)


def crear_token(datos: dict) -> str:
    """
    Genera un JWT con los datos del usuario.
    El token expira según ACCESS_TOKEN_EXPIRE_MINUTES en config.py.
    """
    datos_token = datos.copy()
    expiracion = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    datos_token.update({"exp": expiracion})
    return jwt.encode(datos_token, SECRET_KEY, algorithm=ALGORITHM)


def verificar_token(token: str) -> dict | None:
    """
    Decodifica y valida un JWT.
    Devuelve el payload si es válido, None si no.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
