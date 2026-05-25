"""
config.py — Configuración del backend (FastAPI + MySQL)
Simulador de Laboratorio Virtual - EdTech
Autor: Ortiz Cadena Maria Celeste Camila

Carga variables desde .env para no exponer credenciales en el código.
"""

import os
from dotenv import load_dotenv

load_dotenv()  # Lee el archivo .env si existe

# ── Base de datos ─────────────────────────────────────────
DB_HOST     = os.getenv("DB_HOST",     "localhost")
DB_PORT     = int(os.getenv("DB_PORT", "3306"))
DB_NAME     = os.getenv("DB_NAME",     "lab_virtual")
DB_USER     = os.getenv("DB_USER",     "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")  # Cambia esto a tu contraseña de MySQL

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ── JWT (autenticación con token) ─────────────────────────
SECRET_KEY        = os.getenv("SECRET_KEY", "simulador-virtual-fisica-quimica-123456")
ALGORITHM         = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ── Servidor ──────────────────────────────────────────────
API_HOST = "0.0.0.0"
API_PORT = 8000
