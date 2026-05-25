"""
escenas_ui.py — Escenas de Login y Menú Principal
Simulador de Laboratorio Virtual - EdTech
Autor: Ortiz Cadena Maria Celeste Camila
"""

import pygame
from escenas import Escena
from sesion_usuario import SesionUsuario
from config import (
    ANCHO_PANTALLA, ALTO_PANTALLA,
    COLOR_FONDO, COLOR_BLANCO, COLOR_GRIS_TEXTO,
    COLOR_INPUT_FONDO, COLOR_INPUT_ACTIVO, COLOR_INPUT_IDLE,
    COLOR_BOTON_LOGIN, COLOR_ERROR_TEXTO,
    FUENTE_GRANDE, FUENTE_MEDIANA, FUENTE_PEQUEÑA,
    MAX_CHARS_USUARIO, MAX_CHARS_CONTRASENA,
)


class EscenaLogin(Escena):
    """Pantalla de inicio de sesión de la plataforma."""

    def __init__(self, sesion: SesionUsuario):
        super().__init__("login")
        self._sesion = sesion
        self._fuente_grande = pygame.font.SysFont(*FUENTE_GRANDE)
        # Rectángulos de los campos (para detección de clicks)
        self._rect_username = pygame.Rect(440, 230, 400, 45)
        self._rect_password  = pygame.Rect(440, 310, 400, 45)
        self._rect_boton     = pygame.Rect(540, 390, 200, 50)

    def dibujar(self, pantalla: pygame.Surface) -> None:
        pantalla.fill(COLOR_FONDO)
        self._dibujar_titulo(pantalla)
        self._dibujar_campo(pantalla, "Usuario",    self._rect_username,
                            self._sesion.username, ocultar=False)
        self._dibujar_campo(pantalla, "Contraseña", self._rect_password,
                            self._sesion.password, ocultar=True)
        self._dibujar_boton_entrar(pantalla)
        if self._sesion.hay_error:
            self._dibujar_error(pantalla, self._sesion.mensaje_error)

    def manejar_evento(self, evento: pygame.event.Event) -> str | None:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            return self._manejar_click(evento.pos)
        if evento.type == pygame.KEYDOWN:
            self._manejar_teclado(evento)
        return None

    # ── Dibujo ────────────────────────────────────────────

    def _dibujar_titulo(self, pantalla: pygame.Surface) -> None:
        titulo = self._fuente_grande.render("LABORATORIO VIRTUAL", True, COLOR_BLANCO)
        subtitulo = self._fuente_mediana.render("Iniciar Sesión", True, COLOR_GRIS_TEXTO)
        pantalla.blit(titulo,    (ANCHO_PANTALLA // 2 - titulo.get_width()    // 2, 80))
        pantalla.blit(subtitulo, (ANCHO_PANTALLA // 2 - subtitulo.get_width() // 2, 150))

    def _dibujar_campo(
        self,
        pantalla: pygame.Surface,
        etiqueta: str,
        rect: pygame.Rect,
        valor: str,
        ocultar: bool,
    ) -> None:
        campo_activo = (
            (etiqueta == "Usuario"    and self._sesion.campo_activo == "username") or
            (etiqueta == "Contraseña" and self._sesion.campo_activo == "password")
        )
        borde = COLOR_INPUT_ACTIVO if campo_activo else COLOR_INPUT_IDLE
        pygame.draw.rect(pantalla, COLOR_INPUT_FONDO, rect, border_radius=8)
        pygame.draw.rect(pantalla, borde, rect, 2, border_radius=8)

        lbl = self._fuente_pequeña.render(etiqueta, True, COLOR_GRIS_TEXTO)
        pantalla.blit(lbl, (rect.x + 4, rect.y - 18))

        texto_visible = "*" * len(valor) if ocultar else valor
        txt = self._fuente_mediana.render(texto_visible, True, COLOR_BLANCO)
        pantalla.blit(txt, (rect.x + 12, rect.y + 12))

    def _dibujar_boton_entrar(self, pantalla: pygame.Surface) -> None:
        pygame.draw.rect(pantalla, COLOR_BOTON_LOGIN, self._rect_boton, border_radius=10)
        txt = self._fuente_mediana.render("ENTRAR", True, COLOR_BLANCO)
        pantalla.blit(txt, (
            self._rect_boton.centerx - txt.get_width()  // 2,
            self._rect_boton.centery - txt.get_height() // 2,
        ))

    def _dibujar_error(self, pantalla: pygame.Surface, mensaje: str) -> None:
        err = self._fuente_pequeña.render(mensaje, True, COLOR_ERROR_TEXTO)
        pantalla.blit(err, (ANCHO_PANTALLA // 2 - err.get_width() // 2, 460))

    # ── Eventos ───────────────────────────────────────────

    def _manejar_click(self, pos: tuple) -> str | None:
        if self._rect_username.collidepoint(pos):
            self._sesion.campo_activo = "username"
        elif self._rect_password.collidepoint(pos):
            self._sesion.campo_activo = "password"
        elif self._rect_boton.collidepoint(pos):
            if self._sesion.autenticar():
                return "menu"
        return None

    def _manejar_teclado(self, evento: pygame.event.Event) -> None:
        if evento.key == pygame.K_BACKSPACE:
            self._sesion.borrar_ultimo_caracter()
        elif evento.key == pygame.K_TAB:
            self._sesion.alternar_campo()
        elif evento.key == pygame.K_RETURN:
            self._sesion.autenticar()
        else:
            limite = (
                MAX_CHARS_USUARIO if self._sesion.campo_activo == "username"
                else MAX_CHARS_CONTRASENA
            )
            self._sesion.agregar_caracter(evento.unicode, limite)


class EscenaMenu(Escena):
    """Menú principal de selección de laboratorio."""

    def __init__(self):
        super().__init__("menu")
        self._fuente_grande = pygame.font.SysFont(*FUENTE_GRANDE)
        self._labs = [
            {
                "nombre": "QUÍMICA",
                "subtitulo": "Reacciones y compuestos",
                "destino": "quimica",
                "rect": pygame.Rect(200, 250, 380, 180),
                "color_fondo": (30, 100, 60),
                "color_borde": (50, 180, 100),
                "color_sub":   (180, 255, 180),
            },
            {
                "nombre": "FÍSICA",
                "subtitulo": "Movimiento y fuerzas",
                "destino": "fisica",
                "rect": pygame.Rect(700, 250, 380, 180),
                "color_fondo": (30, 60, 120),
                "color_borde": (50, 100, 220),
                "color_sub":   (180, 180, 255),
            },
        ]

    def dibujar(self, pantalla: pygame.Surface) -> None:
        pantalla.fill(COLOR_FONDO)
        titulo = self._fuente_grande.render(
            "SELECCIONA TU LABORATORIO", True, COLOR_BLANCO
        )
        pantalla.blit(titulo, (ANCHO_PANTALLA // 2 - titulo.get_width() // 2, 80))
        for lab in self._labs:
            self._dibujar_tarjeta_lab(pantalla, lab)

    def manejar_evento(self, evento: pygame.event.Event) -> str | None:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            for lab in self._labs:
                if lab["rect"].collidepoint(evento.pos):
                    return lab["destino"]
        return None

    def _dibujar_tarjeta_lab(self, pantalla: pygame.Surface, lab: dict) -> None:
        pygame.draw.rect(pantalla, lab["color_fondo"], lab["rect"], border_radius=15)
        pygame.draw.rect(pantalla, lab["color_borde"], lab["rect"], 3, border_radius=15)
        centro_x = lab["rect"].centerx
        nombre = self._fuente_grande.render(lab["nombre"], True, COLOR_BLANCO)
        sub    = self._fuente_pequeña.render(lab["subtitulo"], True, lab["color_sub"])
        pantalla.blit(nombre, (centro_x - nombre.get_width() // 2, lab["rect"].y + 70))
        pantalla.blit(sub,    (centro_x - sub.get_width()    // 2, lab["rect"].y + 120))