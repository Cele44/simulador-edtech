"""
COMPONENTE 3: Escena (clase base) + EscenaQuimica + EscenaFisica
Simulador de Laboratorio Virtual - EdTech
Autor: Ortiz Cadena Maria Celeste Camila

RESPONSABILIDAD: Representar cada pantalla/sala del simulador de forma
                 independiente y reutilizable.
REUTILIZABLE EN: Agregar un nuevo laboratorio (biología, astronomía…)
                 solo requiere heredar de Escena e implementar los métodos.

REFACTORIZACIÓN APLICADA:
  - Extract Method: El encabezado (header) y el botón "Volver" se extrajeron
    de las funciones dibujar_quimica() y dibujar_fisica() donde estaban
    duplicados, a métodos heredables de la clase base Escena.
  - Decompose Conditional: El gran if/elif sc == 0/1/2/3 del loop principal
    se reemplazó por polimorfismo: cada escena sabe cómo dibujarse a sí misma.
"""

import pygame
from abc import ABC, abstractmethod
from config import (
    ANCHO_PANTALLA, COLOR_HEADER, COLOR_BLANCO, COLOR_BOTON_VOLVER,
    COLOR_BOTON_TEXTO, FUENTE_MEDIANA, FUENTE_PEQUEÑA,
    TIEMPO_LAB_QUIMICA, TIEMPO_LAB_FISICA
)
from reloj_simulacion import RelojSimulacion


# ══════════════════════════════════════════════════════════
# CLASE BASE — Escena
# ══════════════════════════════════════════════════════════

class Escena(ABC):
    """
    Clase base abstracta para todas las escenas del simulador.

    Cada escena (login, menú, laboratorio) hereda de esta clase
    y solo implementa lo que la hace diferente.  La infraestructura
    compartida (header, botón volver, fuentes) se define aquí una vez.

    REFACTORIZACIÓN — Decompose Conditional:
    En el prototipo, el loop principal tenía:
        if sc == 0: dibujar_login()
        elif sc == 1: dibujar_menu()
        elif sc == 2: dibujar_quimica()
        elif sc == 3: dibujar_fisica()
    Ahora el loop llama a escena_actual.dibujar(pantalla) sin importar
    qué escena sea — el polimorfismo reemplaza al condicional.
    """

    def __init__(self, nombre: str):
        self.nombre = nombre
        self._fuente_mediana = pygame.font.SysFont(*FUENTE_MEDIANA)
        self._fuente_pequeña = pygame.font.SysFont(*FUENTE_PEQUEÑA)

    @abstractmethod
    def dibujar(self, pantalla: pygame.Surface) -> None:
        """Renderiza la escena completa en la pantalla dada."""
        ...

    @abstractmethod
    def manejar_evento(self, evento: pygame.event.Event) -> str | None:
        """
        Procesa un evento pygame.
        Retorna el nombre de la siguiente escena si hay transición,
        o None para quedarse en la escena actual.
        """
        ...

    # ── Métodos reutilizables de UI ───────────────────────

    def _dibujar_header(
        self,
        pantalla: pygame.Surface,
        titulo: str,
        color_fondo: tuple = COLOR_HEADER,
    ) -> None:
        """
        Dibuja el encabezado superior común a todos los laboratorios.

        REFACTORIZACIÓN — Extract Method:
        Estaba copiado y pegado dentro de dibujar_quimica()
        y dibujar_fisica(). Ahora existe una sola vez aquí.
        """
        pygame.draw.rect(pantalla, color_fondo, (0, 0, ANCHO_PANTALLA, 70))
        texto = self._fuente_mediana.render(titulo, True, COLOR_BLANCO)
        pantalla.blit(texto, (20, 22))

    def _dibujar_boton_volver(self, pantalla: pygame.Surface) -> pygame.Rect:
        """
        Dibuja el botón '< VOLVER' y retorna su Rect para detección de clicks.

        REFACTORIZACIÓN — Extract Method:
        También estaba duplicado en ambas funciones de laboratorio.
        """
        rect = pygame.Rect(20, 620, 130, 40)
        pygame.draw.rect(pantalla, COLOR_BOTON_VOLVER, rect, border_radius=8)
        texto = self._fuente_pequeña.render("< VOLVER", True, COLOR_BOTON_TEXTO)
        pantalla.blit(texto, (35, 632))
        return rect

    def _dibujar_reloj(
        self,
        pantalla: pygame.Surface,
        reloj: RelojSimulacion,
        x: int = 1050,
        y: int = 22,
    ) -> None:
        """Renderiza el RelojSimulacion en la posición indicada."""
        texto, color = reloj.formato_display()
        superficie = self._fuente_mediana.render(texto, True, color)
        pantalla.blit(superficie, (x, y))


# ══════════════════════════════════════════════════════════
# ESCENA CONCRETA — Laboratorio de Química
# ══════════════════════════════════════════════════════════

class EscenaQuimica(Escena):
    """
    Laboratorio virtual de química.
    Hereda header, botón volver y reloj de Escena.
    Solo implementa los elementos específicos de química.
    """

    COLOR_FONDO  = (10, 20, 35)
    COLOR_HEADER = (20, 40, 70)

    def __init__(self):
        super().__init__("quimica")
        self.reloj = RelojSimulacion(duracion=TIEMPO_LAB_QUIMICA)
        self._rect_volver: pygame.Rect | None = None

    def iniciar(self) -> None:
        """Llamar cuando se entra a esta escena."""
        self.reloj.iniciar()

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
                return "menu"
        return None

    # ── Dibujo específico de química ──────────────────────

    def _dibujar_mesa(self, pantalla: pygame.Surface) -> None:
        pygame.draw.rect(pantalla, (60, 40, 20), (100, 450, 1080, 30))
        pygame.draw.rect(pantalla, (80, 55, 25), (100, 480, 1080, 15))

    def _dibujar_elementos(self, pantalla: pygame.Surface) -> None:
        self._dibujar_vaso_precipitados(pantalla, x=200, formula="H₂O")
        self._dibujar_tubo_ensayo(pantalla, x=400, formula="NaCl")
        self._dibujar_matraz(pantalla, x=600, formula="H₂SO₄")

    def _dibujar_vaso_precipitados(
        self, pantalla: pygame.Surface, x: int, formula: str
    ) -> None:
        COLOR_VIDRIO = (200, 230, 255)
        COLOR_LIQUIDO = (150, 200, 255)
        pygame.draw.rect(pantalla, COLOR_VIDRIO, (x, 350, 60, 100), 3)
        pygame.draw.rect(pantalla, COLOR_LIQUIDO, (x + 3, 380, 54, 67))
        etiqueta = self._fuente_pequeña.render(formula, True, COLOR_LIQUIDO)
        pantalla.blit(etiqueta, (x + 5, 460))

    def _dibujar_tubo_ensayo(
        self, pantalla: pygame.Surface, x: int, formula: str
    ) -> None:
        COLOR = (200, 150, 255)
        pygame.draw.ellipse(pantalla, COLOR, (x, 340, 40, 15))
        pygame.draw.rect(pantalla, COLOR, (x + 2, 347, 36, 90), 3)
        pygame.draw.ellipse(pantalla, COLOR, (x + 2, 427, 36, 20))
        etiqueta = self._fuente_pequeña.render(formula, True, COLOR)
        pantalla.blit(etiqueta, (x - 5, 460))

    def _dibujar_matraz(
        self, pantalla: pygame.Surface, x: int, formula: str
    ) -> None:
        COLOR = (100, 220, 180)
        pygame.draw.polygon(
            pantalla, COLOR,
            [(x, 440), (x + 80, 440), (x + 60, 360), (x + 20, 360)],
            3,
        )
        pygame.draw.rect(pantalla, COLOR, (x + 28, 320, 24, 42), 3)
        etiqueta = self._fuente_pequeña.render(formula, True, COLOR)
        pantalla.blit(etiqueta, (x + 15, 460))


# ══════════════════════════════════════════════════════════
# ESCENA CONCRETA — Laboratorio de Física
# ══════════════════════════════════════════════════════════

class EscenaFisica(Escena):
    """
    Laboratorio virtual de física.
    Reutiliza toda la infraestructura de Escena;
    solo añade los elementos propios de física.
    """

    COLOR_FONDO  = (10, 15, 30)
    COLOR_HEADER = (20, 30, 60)

    def __init__(self):
        super().__init__("fisica")
        self.reloj = RelojSimulacion(duracion=TIEMPO_LAB_FISICA)
        self._rect_volver: pygame.Rect | None = None
        self._angulo_pendulo: float = 0.0   # para animación futura

    def iniciar(self) -> None:
        self.reloj.iniciar()

    def dibujar(self, pantalla: pygame.Surface) -> None:
        pantalla.fill(self.COLOR_FONDO)
        self._dibujar_header(pantalla, "LABORATORIO DE FÍSICA", self.COLOR_HEADER)
        self._dibujar_reloj(pantalla, self.reloj)
        self._dibujar_mesa(pantalla)
        self._dibujar_pendulo(pantalla)
        self._dibujar_resorte(pantalla)
        self._rect_volver = self._dibujar_boton_volver(pantalla)

    def manejar_evento(self, evento: pygame.event.Event) -> str | None:
        if evento.type == pygame.MOUSEBUTTONDOWN and self._rect_volver:
            if self._rect_volver.collidepoint(evento.pos):
                return "menu"
        return None

    # ── Dibujo específico de física ───────────────────────

    def _dibujar_mesa(self, pantalla: pygame.Surface) -> None:
        pygame.draw.rect(pantalla, (50, 50, 60), (100, 450, 1080, 30))

    def _dibujar_pendulo(self, pantalla: pygame.Surface) -> None:
        COLOR_HILO  = (200, 200, 200)
        COLOR_BOLA  = (220, 180, 50)
        PIVOT_X, PIVOT_Y = 640, 150
        BOLA_Y = 360
        pygame.draw.line(pantalla, COLOR_HILO, (PIVOT_X, PIVOT_Y), (PIVOT_X, BOLA_Y), 3)
        pygame.draw.circle(pantalla, COLOR_BOLA, (PIVOT_X, BOLA_Y + 10), 25)
        etiqueta = self._fuente_pequeña.render("Péndulo Simple", True, COLOR_HILO)
        pantalla.blit(etiqueta, (PIVOT_X - 50, 400))

    def _dibujar_resorte(self, pantalla: pygame.Surface) -> None:
        COLOR_RESORTE = (150, 200, 150)
        for i in range(10):
            y_base = 280 + i * 15
            x_izq  = 300 + (i % 2) * 30
            x_der  = 330 - (i % 2) * 30
            pygame.draw.line(
                pantalla, COLOR_RESORTE,
                (x_izq, y_base), (x_der, y_base + 15),
                2,
            )
        etiqueta = self._fuente_pequeña.render("Resorte", True, COLOR_RESORTE)
        pantalla.blit(etiqueta, (295, 460))