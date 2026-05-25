"""
database.py — Conexión a MySQL con SQLAlchemy
Simulador de Laboratorio Virtual - EdTech
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # Verifica que la conexión sigue activa
    echo=False,           # Cambia a True para ver las queries SQL en consola
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Dependencia de FastAPI: abre una sesión de BD por request
    y la cierra automáticamente al terminar.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
