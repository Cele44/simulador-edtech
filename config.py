"""
config.py — Configuración global de la plataforma
Simulador de Laboratorio Virtual - EdTech
Autor: Ortiz Cadena Maria Celeste Camila

REFACTORIZACIÓN APLICADA: Replace Magic Number
Todos los valores literales que aparecían dispersos en el prototipo
se centralizan aquí con nombres descriptivos.
"""

# ── Pantalla ──────────────────────────────────────────────
ANCHO_PANTALLA = 1280
ALTO_PANTALLA  = 720
FPS            = 60

# ── Colores del sistema ───────────────────────────────────
COLOR_FONDO        = (15, 15, 40)
COLOR_FONDO_LAB    = (10, 20, 35)
COLOR_HEADER       = (20, 40, 70)
COLOR_BLANCO       = (255, 255, 255)
COLOR_GRIS_TEXTO   = (180, 180, 200)
COLOR_ADVERTENCIA  = (255, 80,  80)
COLOR_RELOJ_NORMAL = (255, 220, 100)
COLOR_RELOJ_ALERTA = (255, 80,  80)
COLOR_BOTON_VOLVER = (80,  30,  30)
COLOR_BOTON_TEXTO  = (255, 200, 200)
COLOR_INPUT_ACTIVO = (100, 150, 255)
COLOR_INPUT_IDLE   = (80,  80,  120)
COLOR_INPUT_FONDO  = (50,  50,  80)
COLOR_BOTON_LOGIN  = (50,  100, 200)
COLOR_ERROR_TEXTO  = (255, 100, 100)

# ── Tiempos de laboratorio (segundos) ────────────────────
TIEMPO_LAB_QUIMICA = 300   # 5 minutos
TIEMPO_LAB_FISICA  = 600   # 10 minutos
UMBRAL_ALERTA      = 60    # segundos restantes para cambiar color

# ── Fuentes ───────────────────────────────────────────────
FUENTE_GRANDE  = ("arial", 32)
FUENTE_MEDIANA = ("arial", 20)
FUENTE_PEQUEÑA = ("arial", 16)

# ── Límites de texto ──────────────────────────────────────
MAX_CHARS_USUARIO    = 20
MAX_CHARS_CONTRASENA = 20

# ── Escenas ───────────────────────────────────────────────
ESCENA_LOGIN   = 0
ESCENA_MENU    = 1
ESCENA_QUIMICA = 2
ESCENA_FISICA  = 3

# ── Usuarios del sistema (en producción vendría de una BD) ─
USUARIOS_SISTEMA = {
    "estudiante": "1234",
    "admin":      "admin123",
}