"""
api_client.py — Cliente HTTP para conectar el frontend (Pygame) con el backend (FastAPI)
Simulador de Laboratorio Virtual - EdTech
Autor: Ortiz Cadena Maria Celeste Camila

Este archivo reemplaza la autenticación local que estaba en config.py (USUARIOS_SISTEMA).
Ahora las credenciales se validan en el servidor, y las interacciones se guardan en MySQL.
"""

import requests
from typing import Optional

# ── URL base del backend ──────────────────────────────────
# Si corres el backend en otra máquina, cambia "localhost" por la IP de ese equipo
BASE_URL = "http://localhost:8000"


class APIClient:
    """
    Encapsula todas las llamadas HTTP al backend FastAPI.
    Se instancia una vez y se reutiliza durante toda la sesión.
    """

    def __init__(self):
        self._token: Optional[str] = None
        self._username: str = ""
        self._rol: str = ""
        self._interaccion_activa_id: Optional[int] = None

    # ── Autenticación ─────────────────────────────────────

    def login(self, username: str, password: str) -> tuple[bool, str]:
        """
        Intenta autenticar al usuario contra el backend.

        Retorna:
            (True, "")          si el login fue exitoso
            (False, "mensaje")  si falló, con el motivo
        """
        try:
            respuesta = requests.post(
                f"{BASE_URL}/auth/login",
                json={"username": username, "password": password},
                timeout=5,
            )
            if respuesta.status_code == 200:
                datos = respuesta.json()
                self._token    = datos["access_token"]
                self._username = datos["username"]
                self._rol      = datos["rol"]
                return True, ""
            elif respuesta.status_code == 401:
                return False, "Usuario o contraseña incorrectos"
            else:
                return False, f"Error del servidor: {respuesta.status_code}"
        except requests.exceptions.ConnectionError:
            return False, "No se puede conectar al servidor"
        except requests.exceptions.Timeout:
            return False, "El servidor tardó demasiado en responder"

    def cerrar_sesion(self) -> None:
        self._token               = None
        self._username            = ""
        self._rol                 = ""
        self._interaccion_activa_id = None

    # ── Laboratorios ──────────────────────────────────────

    def iniciar_laboratorio(self, laboratorio: str) -> Optional[int]:
        """
        Registra en la BD que el estudiante entró a un laboratorio.
        Devuelve el ID de la interacción (necesario para finalizarla).

        laboratorio: "quimica" | "fisica"
        """
        if not self._token:
            return None
        try:
            respuesta = requests.post(
                f"{BASE_URL}/labs/iniciar",
                json={"laboratorio": laboratorio},
                headers=self._cabeceras(),
                timeout=5,
            )
            if respuesta.status_code == 200:
                self._interaccion_activa_id = respuesta.json()["id"]
                return self._interaccion_activa_id
        except requests.exceptions.RequestException:
            pass  # Si falla la red, el juego sigue funcionando igual
        return None

    def finalizar_laboratorio(self, duracion_segundos: int, completo: bool) -> bool:
        """
        Registra en la BD que el estudiante salió del laboratorio.
        Se llama al presionar VOLVER o al agotarse el tiempo.
        """
        if not self._token or not self._interaccion_activa_id:
            return False
        try:
            respuesta = requests.put(
                f"{BASE_URL}/labs/finalizar",
                json={
                    "interaccion_id":    self._interaccion_activa_id,
                    "duracion_segundos": duracion_segundos,
                    "completo":          completo,
                },
                headers=self._cabeceras(),
                timeout=5,
            )
            if respuesta.status_code == 200:
                self._interaccion_activa_id = None
                return True
        except requests.exceptions.RequestException:
            pass
        return False

    # ── Propiedades públicas ──────────────────────────────

    @property
    def autenticado(self) -> bool:
        return self._token is not None

    @property
    def username(self) -> str:
        return self._username

    @property
    def rol(self) -> str:
        return self._rol

    # ── Interno ───────────────────────────────────────────

    def _cabeceras(self) -> dict:
        return {"Authorization": f"Bearer {self._token}"}


# Instancia global: todo el frontend usa este mismo objeto
api = APIClient()
