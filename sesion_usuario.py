"""
COMPONENTE 1: SesionUsuario
Simulador de Laboratorio Virtual - EdTech
Autor: Ortiz Cadena Maria Celeste Camila

RESPONSABILIDAD: Gestionar el estado de autenticación del usuario.
REUTILIZABLE EN: Cualquier laboratorio de la plataforma (química, física, biología…)

REFACTORIZACIÓN APLICADA:
  - Extract Method: La validación de credenciales se extrajo del loop
    principal a un método dedicado `autenticar()`.
  - Rename Variable: n→username, pw→password, log→autenticado,
    sc→escena_actual.
"""

from config import USUARIOS_SISTEMA, ESCENA_LOGIN, ESCENA_MENU


class SesionUsuario:
    """
    Gestiona el ciclo de vida de la sesión de un estudiante.
    Encapsula: estado de login, campo activo, mensajes de error.
    """

    def __init__(self):
        self.username: str   = ""
        self.password: str   = ""
        self.autenticado: bool = False
        self.campo_activo: str = "username"   # "username" | "password"
        self.mensaje_error: str = ""

    # ── Métodos de autenticación ──────────────────────────

    def autenticar(self) -> bool:
        """
        Valida las credenciales contra el repositorio de usuarios.
        Retorna True si el acceso fue concedido.

        REFACTORIZACIÓN — Extract Method:
        En el prototipo, esta lógica estaba incrustada directamente
        dentro del bloque MOUSEBUTTONDOWN del loop principal, mezclando
        captura de eventos con lógica de negocio.
        """
        if self.username in USUARIOS_SISTEMA:
            if USUARIOS_SISTEMA[self.username] == self.password:
                self.autenticado = True
                self.mensaje_error = ""
                return True
        self.mensaje_error = "Usuario o contraseña incorrectos"
        return False

    def cerrar_sesion(self) -> None:
        """Resetea el estado de sesión por completo."""
        self.username     = ""
        self.password     = ""
        self.autenticado  = False
        self.campo_activo = "username"
        self.mensaje_error = ""

    # ── Métodos de entrada de texto ───────────────────────

    def alternar_campo(self) -> None:
        """Cambia el foco entre los campos usuario y contraseña."""
        self.campo_activo = (
            "password" if self.campo_activo == "username" else "username"
        )

    def agregar_caracter(self, caracter: str, limite: int) -> None:
        """
        Agrega un carácter al campo activo respetando el límite.

        REFACTORIZACIÓN — Extract Method:
        En el prototipo había dos bloques if duplicados para cada campo.
        Ahora un único método maneja ambos casos.
        """
        if self.campo_activo == "username":
            if len(self.username) < limite:
                self.username += caracter
        else:
            if len(self.password) < limite:
                self.password += caracter

    def borrar_ultimo_caracter(self) -> None:
        """Elimina el último carácter del campo activo."""
        if self.campo_activo == "username":
            self.username = self.username[:-1]
        else:
            self.password = self.password[:-1]

    # ── Propiedades de consulta ───────────────────────────

    @property
    def nombre_usuario(self) -> str:
        return self.username

    @property
    def hay_error(self) -> bool:
        return bool(self.mensaje_error)