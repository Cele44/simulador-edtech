"""
crear_usuarios.py — Script para poblar la BD con usuarios iniciales
Simulador de Laboratorio Virtual - EdTech
Autor: Ortiz Cadena Maria Celeste Camila

Ejecutar UNA SOLA VEZ desde la carpeta backend/:
    python ../crear_usuarios.py
    
O desde la raíz del proyecto:
    python crear_usuarios.py
"""

import sys
import os

# Para que encuentre los módulos del backend
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from database import SessionLocal, engine, Base
from app.models.estudiante import Estudiante
from app.models.interaccion import InteraccionLab
from app.services.auth_service import hashear_password

# ══════════════════════════════════════════════════════════
# LISTA DE USUARIOS — Agrega aquí todos los que necesites
# ══════════════════════════════════════════════════════════

USUARIOS = [
    {
        "username":        "admin",
        "password":        "admin123",
        "nombre_completo": "Administrador del Sistema",
        "email":           "admin@lab.edu",
        "rol":             "admin",
    },
    {
        "username":        "maria.fernandez",
        "password":        "1234",
        "nombre_completo": "María Fernández García",
        "email":           "maria.fernandez@lab.edu",
        "rol":             "estudiante",
    },
    # ── Agrega más estudiantes aquí con el mismo formato ──
    # {
    #     "username":        "maria_perez",
    #     "password":        "clave123",
    #     "nombre_completo": "María Pérez",
    #     "email":           "maria@lab.edu",
    #     "rol":             "estudiante",
    # },
]

# ══════════════════════════════════════════════════════════

def crear_tablas():
    """Crea las tablas si no existen (seguro de correr varias veces)."""
    Base.metadata.create_all(bind=engine)
    print("✓ Tablas verificadas/creadas en la BD")


def limpiar_estudiantes(db):
    """Borra todos los estudiantes existentes para empezar limpio."""
    db.query(InteraccionLab).delete()
    db.query(Estudiante).delete()
    db.commit()
    print("✓ Tabla estudiantes limpiada")


def crear_usuarios(db):
    """Inserta los usuarios con contraseñas hasheadas correctamente."""
    creados = 0
    omitidos = 0

    for datos in USUARIOS:
        # Verifica si ya existe para no duplicar
        existente = db.query(Estudiante).filter(
            Estudiante.username == datos["username"]
        ).first()

        if existente:
            print(f"  ⚠ '{datos['username']}' ya existe — omitido")
            omitidos += 1
            continue

        estudiante = Estudiante(
            username        = datos["username"],
            password_hash   = hashear_password(datos["password"]),  # ← hash bcrypt real
            nombre_completo = datos.get("nombre_completo"),
            email           = datos.get("email"),
            rol             = datos.get("rol", "estudiante"),
        )
        db.add(estudiante)
        creados += 1
        print(f"  ✓ '{datos['username']}' creado con rol '{datos['rol']}'")

    db.commit()
    print(f"\n✓ Proceso terminado: {creados} creados, {omitidos} omitidos")


def main():
    print("\n=== Configurando usuarios del Laboratorio Virtual ===\n")
    crear_tablas()

    db = SessionLocal()
    try:
        #limpiar_estudiantes(db)
        print("\nCreando usuarios:")
        crear_usuarios(db)
    finally:
        db.close()

    print("\n=== Listo. Ya puedes iniciar sesión en el simulador ===\n")


if __name__ == "__main__":
    main()