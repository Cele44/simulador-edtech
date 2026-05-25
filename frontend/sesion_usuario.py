"""
sesion_usuario.py — Gestión de sesión del estudiante
Simulador de Laboratorio Virtual - EdTech
Autor: Ortiz Cadena Maria Celeste Camila

CAMBIO PRINCIPAL respecto a la versión anterior:
  Antes: autenticar() comparaba contra el diccionario USUARIOS_SISTEMA en config.py
  Ahora: autenticar() llama a api.login() que consulta la base de datos MySQL
         a través del backend FastAPI.

Todo lo demás (manejo de campos, errores, etc.) queda igual.
"""

from api_client import api   # ← único cambio de importación
from config import MAX_CHARS_USUARIO, MAX_CHARS_CONTRASENA


class SesionUsuario:
    """
    Gestiona el ciclo de vida de la sesión de un estudiante.
    Encapsula: estado de login, campo activo, mensajes de error.
    """

    def __init__(self):
        self.username: str    = ""
        self.password: str    = ""
        self.campo_activo: str = "username"   # "username" | "password"
        self.mensaje_error: str = ""

    # ── Métodos de autenticación ──────────────────────────

    def autenticar(self) -> bool:
        """
        Valida las credenciales contra el backend (que consulta MySQL).
        Retorna True si el acceso fue concedido.
        """
        exito, mensaje = api.login(self.username, self.password)
        if exito:
            self.mensaje_error = ""
            return True
        self.mensaje_error = mensaje or "Usuario o contraseña incorrectos"
        return False

    def cerrar_sesion(self) -> None:
        """Resetea el estado de sesión por completo."""
        self.username      = ""
        self.password      = ""
        self.campo_activo  = "username"
        self.mensaje_error = ""
        api.cerrar_sesion()   # También limpia el token en el cliente HTTP

    # ── Métodos de entrada de texto ───────────────────────

    def alternar_campo(self) -> None:
        self.campo_activo = (
            "password" if self.campo_activo == "username" else "username"
        )

    def agregar_caracter(self, caracter: str, limite: int) -> None:
        if self.campo_activo == "username":
            if len(self.username) < limite:
                self.username += caracter
        else:
            if len(self.password) < limite:
                self.password += caracter

    def borrar_ultimo_caracter(self) -> None:
        if self.campo_activo == "username":
            self.username = self.username[:-1]
        else:
            self.password = self.password[:-1]

    # ── Propiedades de consulta ───────────────────────────

    @property
    def autenticado(self) -> bool:
        return api.autenticado

    @property
    def nombre_usuario(self) -> str:
        return api.username or self.username

    @property
    def hay_error(self) -> bool:
        return bool(self.mensaje_error)
