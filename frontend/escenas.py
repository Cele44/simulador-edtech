"""
COMPONENTE 3: Escena (clase base) + EscenaQuimica + EscenaFisica
Simulador de Laboratorio Virtual - EdTech
Autor: Ortiz Cadena Maria Celeste Camila

REFACTORIZACIÓN APLICADA:
  - Extract Method: header, botón volver y reloj definidos una sola vez.
  - Decompose Conditional: polimorfismo reemplaza el if/elif de escenas.

ACTUALIZACIÓN: Integración de ObjetoLab (Componente 4).
ACTUALIZACIÓN 2: Registro de interacciones en MySQL vía API.
  - iniciar()           → POST /labs/iniciar    (guarda fecha_inicio en BD)
  - _registrar_salida() → PUT  /labs/finalizar  (guarda duración y fecha_fin)
"""

import pygame
from abc import ABC, abstractmethod
from config import (
    ANCHO_PANTALLA, COLOR_HEADER, COLOR_BLANCO, COLOR_BOTON_VOLVER,
    COLOR_BOTON_TEXTO, FUENTE_MEDIANA, FUENTE_PEQUEÑA,
    TIEMPO_LAB_QUIMICA, TIEMPO_LAB_FISICA
)
from reloj_simulacion import RelojSimulacion
from objeto_lab import VasoPrecipitados, TuboEnsayo, Matraz, Pendulo, Resorte
from api_client import api


# ══════════════════════════════════════════════════════════
# CLASE BASE — Escena
# ══════════════════════════════════════════════════════════

class Escena(ABC):

    def __init__(self, nombre: str):
        self.nombre = nombre
        self._fuente_mediana = pygame.font.SysFont(*FUENTE_MEDIANA)
        self._fuente_pequeña = pygame.font.SysFont(*FUENTE_PEQUEÑA)

    @abstractmethod
    def dibujar(self, pantalla: pygame.Surface) -> None: ...

    @abstractmethod
    def manejar_evento(self, evento: pygame.event.Event) -> str | None: ...

    def actualizar(self, dt: float) -> None:
        pass

    def _dibujar_header(self, pantalla, titulo, color_fondo=COLOR_HEADER):
        pygame.draw.rect(pantalla, color_fondo, (0, 0, ANCHO_PANTALLA, 70))
        texto = self._fuente_mediana.render(titulo, True, COLOR_BLANCO)
        pantalla.blit(texto, (20, 22))

    def _dibujar_boton_volver(self, pantalla) -> pygame.Rect:
        rect = pygame.Rect(20, 620, 130, 40)
        pygame.draw.rect(pantalla, COLOR_BOTON_VOLVER, rect, border_radius=8)
        texto = self._fuente_pequeña.render("< VOLVER", True, COLOR_BOTON_TEXTO)
        pantalla.blit(texto, (35, 632))
        return rect

    def _dibujar_reloj(self, pantalla, reloj, x=1050, y=22):
        texto, color = reloj.formato_display()
        superficie = self._fuente_mediana.render(texto, True, color)
        pantalla.blit(superficie, (x, y))


# ══════════════════════════════════════════════════════════
# ESCENA — Laboratorio de Química
# ══════════════════════════════════════════════════════════

class EscenaQuimica(Escena):

    COLOR_FONDO  = (10, 20, 35)
    COLOR_HEADER = (20, 40, 70)
    MESA_Y       = 450

    def __init__(self):
        super().__init__("quimica")
        self.reloj           = RelojSimulacion(duracion=TIEMPO_LAB_QUIMICA)
        self._rect_volver    = None
        self._interaccion_id = None

        self._vaso   = VasoPrecipitados(x=250, y=self.MESA_Y - 100,
                                        formula="H2O",
                                        velocidad=1.5, amplitud=6.0)
        self._tubo   = TuboEnsayo(x=550, y=self.MESA_Y - 107,
                                  formula="NaCl",
                                  velocidad=8.0, intensidad=4.0)
        self._matraz = Matraz(x=850, y=self.MESA_Y - 120,
                              formula="H2SO4",
                              velocidad_color=0.4)

    def iniciar(self) -> None:
        """Arranca el reloj y registra en la BD que el estudiante entró."""
        self.reloj.iniciar()
        self._interaccion_id = api.iniciar_laboratorio("quimica")

    def actualizar(self, dt: float) -> None:
        """Actualiza objetos y detecta si el tiempo se agotó."""
        self._vaso.actualizar(dt)
        self._tubo.actualizar(dt)
        self._matraz.actualizar(dt)
        if self.reloj.esta_vencido() and self._interaccion_id:
            self._registrar_salida(completo=True)

    def dibujar(self, pantalla: pygame.Surface) -> None:
        pantalla.fill(self.COLOR_FONDO)
        self._dibujar_header(pantalla, "LABORATORIO DE QUÍMICA", self.COLOR_HEADER)
        self._dibujar_reloj(pantalla, self.reloj)
        self._dibujar_mesa(pantalla)
        self._dibujar_elementos(pantalla)
        self._rect_volver = self._dibujar_boton_volver(pantalla)

    def manejar_evento(self, evento: pygame.event.Event) -> str | None:
        if evento.type == pygame.MOUSEBUTTONDOWN and self._rect_volver:
            if self._rect_volver.collidepoint(evento.pos):
                self._registrar_salida(completo=False)
                return "menu"
        return None

    def _registrar_salida(self, completo: bool) -> None:
        """Guarda en la BD cuánto tiempo estuvo y si completó el lab."""
        if self._interaccion_id is None:
            return
        duracion = int(self.reloj.duracion_total - self.reloj.segundos_restantes())
        api.finalizar_laboratorio(duracion_segundos=duracion, completo=completo)
        self._interaccion_id = None

    def _dibujar_mesa(self, pantalla):
        pygame.draw.rect(pantalla, (60, 40, 20), (100, self.MESA_Y,      1080, 30))
        pygame.draw.rect(pantalla, (80, 55, 25), (100, self.MESA_Y + 30, 1080, 15))

    def _dibujar_elementos(self, pantalla):
        self._vaso.dibujar(pantalla)
        self._tubo.dibujar(pantalla)
        self._matraz.dibujar(pantalla)


# ══════════════════════════════════════════════════════════
# ESCENA — Laboratorio de Física
# ══════════════════════════════════════════════════════════

class EscenaFisica(Escena):

    COLOR_FONDO  = (10, 15, 30)
    COLOR_HEADER = (20, 30, 60)
    MESA_Y       = 450

    def __init__(self):
        super().__init__("fisica")
        self.reloj           = RelojSimulacion(duracion=TIEMPO_LAB_FISICA)
        self._rect_volver    = None
        self._interaccion_id = None

        self._pendulo = Pendulo(x=400, y=100,
                                longitud=280.0,
                                amplitud_deg=30.0,
                                gravedad=9.8)
        self._resorte = Resorte(x=800, y=100,
                                masa=1.0,
                                constante_k=40.0,
                                amplitud=30.0)

    def iniciar(self) -> None:
        """Arranca el reloj y registra en la BD que el estudiante entró."""
        self.reloj.iniciar()
        self._interaccion_id = api.iniciar_laboratorio("fisica")

    def actualizar(self, dt: float) -> None:
        """Actualiza objetos y detecta si el tiempo se agotó."""
        self._pendulo.actualizar(dt)
        self._resorte.actualizar(dt)
        if self.reloj.esta_vencido() and self._interaccion_id:
            self._registrar_salida(completo=True)

    def dibujar(self, pantalla: pygame.Surface) -> None:
        pantalla.fill(self.COLOR_FONDO)
        self._dibujar_header(pantalla, "LABORATORIO DE FÍSICA", self.COLOR_HEADER)
        self._dibujar_reloj(pantalla, self.reloj)
        self._dibujar_techo(pantalla)
        self._dibujar_mesa(pantalla)
        self._pendulo.dibujar(pantalla)
        self._resorte.dibujar(pantalla)
        self._rect_volver = self._dibujar_boton_volver(pantalla)

    def manejar_evento(self, evento: pygame.event.Event) -> str | None:
        if evento.type == pygame.MOUSEBUTTONDOWN and self._rect_volver:
            if self._rect_volver.collidepoint(evento.pos):
                self._registrar_salida(completo=False)
                return "menu"
        return None

    def _registrar_salida(self, completo: bool) -> None:
        """Guarda en la BD cuánto tiempo estuvo y si completó el lab."""
        if self._interaccion_id is None:
            return
        duracion = int(self.reloj.duracion_total - self.reloj.segundos_restantes())
        api.finalizar_laboratorio(duracion_segundos=duracion, completo=completo)
        self._interaccion_id = None

    def _dibujar_techo(self, pantalla):
        pygame.draw.rect(pantalla, (80, 80, 100), (100, 90, 1080, 14))

    def _dibujar_mesa(self, pantalla):
        pygame.draw.rect(pantalla, (50, 50, 60), (100, self.MESA_Y,      1080, 30))
        pygame.draw.rect(pantalla, (70, 70, 85), (100, self.MESA_Y + 30, 1080, 12))