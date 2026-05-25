"""
COMPONENTE 4: ObjetoLab (clase base) + objetos concretos
Simulador de Laboratorio Virtual - EdTech
Autor: Ortiz Cadena Maria Celeste Camila

RESPONSABILIDAD:
    Representar cualquier objeto interactivo de un laboratorio.
    Cada objeto sabe cómo dibujarse y cómo moverse, según su
    naturaleza física o química.

REUTILIZABLE EN:
    Cualquier laboratorio. Agregar un nuevo objeto =
    crear una subclase de ObjetoLab e implementar
    actualizar() y dibujar().

PRINCIPIO APLICADO:
    Open/Closed — el sistema está abierto para agregar objetos
    nuevos sin modificar el código existente.

MOVIMIENTOS IMPLEMENTADOS:
    Química  (base del objeto en self.y, base apoyada sobre la mesa):
        VasoPrecipitados  alto=100  → oscilación lateral suave en X
        TuboEnsayo        alto=107  → vibración horizontal con pulso
        Matraz            alto=120  → cambio cíclico de color

    Física   (pivot/ancla en self.y, cuelgan hacia abajo):
        Pendulo           → ángulo senoidal real  ω = √(g/L)
        Resorte           → compresión/extensión  ω = √(k/m)
"""

import math
import pygame
from abc import ABC, abstractmethod


# ══════════════════════════════════════════════════════════
#  CLASE BASE — ObjetoLab
# ══════════════════════════════════════════════════════════

class ObjetoLab(ABC):
    """
    Contrato base para todos los objetos animados del laboratorio.

    Cada subclase define:
        - Su propia lógica de movimiento en actualizar()
        - Su propio dibujado en dibujar()

    El laboratorio solo llama a:
        objeto.actualizar(dt)
        objeto.dibujar(pantalla)
    Sin importar qué tipo de objeto sea.
    """

    def __init__(self, x: float, y: float, etiqueta: str = ""):
        self.x        = x
        self.y        = y
        self.etiqueta = etiqueta
        self.activo   = True
        self.tiempo   = 0.0
        self._fuente  = pygame.font.SysFont("arial", 14)

    @abstractmethod
    def actualizar(self, dt: float) -> None: ...

    @abstractmethod
    def dibujar(self, pantalla: pygame.Surface) -> None: ...

    def activar(self)    -> None: self.activo = True
    def desactivar(self) -> None: self.activo = False

    def _dibujar_etiqueta(self, pantalla, dx=0, dy=20, color=(200, 200, 200)):
        if self.etiqueta:
            txt = self._fuente.render(self.etiqueta, True, color)
            pantalla.blit(txt, (int(self.x) + dx - txt.get_width() // 2,
                                int(self.y) + dy))

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}"
                f"(x={self.x:.0f}, y={self.y:.0f}, etiqueta='{self.etiqueta}')")


# ══════════════════════════════════════════════════════════
#  OBJETOS DE QUÍMICA
#  Convención: self.y = borde SUPERIOR del objeto
#              base del objeto queda en self.y + alto
#              → EscenaQuimica pasa y = MESA_Y - alto
# ══════════════════════════════════════════════════════════

class VasoPrecipitados(ObjetoLab):
    """
    Vaso de precipitados apoyado sobre la mesa.
    Alto total = 100 px  →  base en self.y + 100 = MESA_Y.
    Movimiento: oscilación lateral suave en X.
    """

    ANCHO         = 60
    ALTO          = 100
    COLOR_VIDRIO  = (200, 230, 255)
    COLOR_LIQUIDO = (150, 200, 255)

    def __init__(self, x: float, y: float, formula: str = "H2O",
                 velocidad: float = 1.5, amplitud: float = 6.0):
        super().__init__(x, y, formula)
        self.velocidad = velocidad
        self.amplitud  = amplitud
        self._offset_x = 0.0

    def actualizar(self, dt: float) -> None:
        if not self.activo:
            return
        self.tiempo    += dt * self.velocidad
        self._offset_x  = math.sin(self.tiempo) * self.amplitud

    def dibujar(self, pantalla: pygame.Surface) -> None:
        if not self.activo:
            return
        ox = int(self.x + self._offset_x)
        oy = int(self.y)

        # Líquido interior (arranca en y+30, 67px de alto)
        pygame.draw.rect(pantalla, self.COLOR_LIQUIDO,
                         (ox + 3, oy + 30, self.ANCHO - 6, 67))
        # Contorno del vaso (60x100, grosor 3)
        pygame.draw.rect(pantalla, self.COLOR_VIDRIO,
                         (ox, oy, self.ANCHO, self.ALTO), 3)
        # Boca del vaso
        pygame.draw.line(pantalla, self.COLOR_VIDRIO,
                         (ox - 4, oy), (ox + self.ANCHO + 4, oy), 2)

        # Etiqueta debajo de la base (fuera de la mesa, no ocluida)
        self._dibujar_etiqueta(pantalla, dx=self.ANCHO // 2,
                               dy=self.ALTO + 6, color=self.COLOR_LIQUIDO)


class TuboEnsayo(ObjetoLab):
    """
    Tubo de ensayo apoyado sobre la mesa.
    Alto total = 107 px  →  base en self.y + 107 = MESA_Y.
    Movimiento: vibración horizontal con pulso.
    """

    ANCHO = 40
    ALTO  = 107     # elipse_sup(15) + rect(90) + punta(redondeada ≈2)
    COLOR = (200, 150, 255)

    def __init__(self, x: float, y: float, formula: str = "NaCl",
                 velocidad: float = 8.0, intensidad: float = 4.0):
        super().__init__(x, y, formula)
        self.velocidad  = velocidad
        self.intensidad = intensidad
        self._offset_x  = 0.0
        self._pulso     = 0.0

    def actualizar(self, dt: float) -> None:
        if not self.activo:
            return
        self.tiempo    += dt
        self._pulso     = abs(math.sin(self.tiempo * 0.8))
        self._offset_x  = (math.sin(self.tiempo * self.velocidad)
                           * self.intensidad * self._pulso)

    def dibujar(self, pantalla: pygame.Surface) -> None:
        if not self.activo:
            return
        ox = int(self.x + self._offset_x)
        oy = int(self.y)

        # Boca (elipse 40x15 en la parte superior)
        pygame.draw.ellipse(pantalla, self.COLOR, (ox, oy, 40, 15))
        # Cuerpo (rect 36x90, grosor 3)
        pygame.draw.rect(pantalla, self.COLOR, (ox + 2, oy + 7, 36, 90), 3)
        # Fondo redondeado (elipse 36x20 al final del cuerpo)
        pygame.draw.ellipse(pantalla, self.COLOR, (ox + 2, oy + 87, 36, 20))

        self._dibujar_etiqueta(pantalla, dx=self.ANCHO // 2,
                               dy=self.ALTO + 6, color=self.COLOR)


class Matraz(ObjetoLab):
    """
    Matraz Erlenmeyer apoyado sobre la mesa.
    Alto total = 120 px  →  base en self.y + 120 = MESA_Y.
      Cuello: 36px (rect 24x36 desde self.y)
      Cuerpo: 80px (trapecio de self.y+36 a self.y+116)
      Base:    4px de margen
    Movimiento: cambio cíclico de color del líquido.
    """

    ALTO           = 120
    COLOR_CONTORNO = (100, 220, 180)

    def __init__(self, x: float, y: float, formula: str = "H2SO4",
                 velocidad_color: float = 0.4):
        super().__init__(x, y, formula)
        self.velocidad_color = velocidad_color
        self._color_liquido  = (100, 220, 180)

    def _calcular_color(self) -> tuple:
        t = self.tiempo
        r = int(100 + 100 * math.sin(t))
        g = int(180 +  40 * math.sin(t + 2.1))
        b = int(150 +  60 * math.sin(t + 4.2))
        return (max(0, min(255, r)),
                max(0, min(255, g)),
                max(0, min(255, b)))

    def actualizar(self, dt: float) -> None:
        if not self.activo:
            return
        self.tiempo         += dt * self.velocidad_color
        self._color_liquido  = self._calcular_color()

    def dibujar(self, pantalla: pygame.Surface) -> None:
        if not self.activo:
            return
        ox = int(self.x)
        oy = int(self.y)

        # Cuello (rect 24x36 centrado, desde self.y)
        pygame.draw.rect(pantalla, self.COLOR_CONTORNO,
                         (ox + 28, oy, 24, 36), 3)

        # Cuerpo trapezoidal (80px de alto, debajo del cuello)
        # vértices: base ancha en oy+116, hombros en oy+36
        cuerpo = [(ox,      oy + 116),
                  (ox + 80, oy + 116),
                  (ox + 60, oy +  36),
                  (ox + 20, oy +  36)]
        pygame.draw.polygon(pantalla, self._color_liquido, cuerpo)
        pygame.draw.polygon(pantalla, self.COLOR_CONTORNO,  cuerpo, 3)

        # Burbujas animadas dentro del cuerpo
        for i in range(3):
            bx = ox + 18 + i * 18
            by = oy + 80 - int(18 * abs(math.sin(self.tiempo + i * 1.0)))
            pygame.draw.circle(pantalla, (255, 255, 255), (bx, by), 3)

        self._dibujar_etiqueta(pantalla, dx=40, dy=self.ALTO + 6,
                               color=self.COLOR_CONTORNO)


# ══════════════════════════════════════════════════════════
#  OBJETOS DE FÍSICA
#  Convención: self.x, self.y = punto de anclaje (pivot/techo)
#              el objeto cuelga hacia abajo desde ese punto
# ══════════════════════════════════════════════════════════

class Pendulo(ObjetoLab):
    """
    Péndulo simple colgado del techo.
    Pivot en (self.x, self.y).
    Movimiento: ángulo senoidal real  ω = √(g/L).
    """

    COLOR_HILO = (200, 200, 200)
    COLOR_BOLA = (220, 180,  50)

    def __init__(self, x: float, y: float, longitud: float = 280.0,
                 amplitud_deg: float = 30.0, gravedad: float = 9.8):
        super().__init__(x, y, "Péndulo Simple")
        self.longitud     = longitud
        self.amplitud_rad = math.radians(amplitud_deg)
        self._frecuencia  = math.sqrt(gravedad / longitud)
        self._bola_x      = x
        self._bola_y      = y + longitud

    def actualizar(self, dt: float) -> None:
        if not self.activo:
            return
        self.tiempo  += dt
        angulo        = self.amplitud_rad * math.cos(
                            self._frecuencia * self.tiempo)
        self._bola_x  = self.x + self.longitud * math.sin(angulo)
        self._bola_y  = self.y + self.longitud * math.cos(angulo)

    def dibujar(self, pantalla: pygame.Surface) -> None:
        if not self.activo:
            return
        pivot = (int(self.x),       int(self.y))
        bola  = (int(self._bola_x), int(self._bola_y))

        pygame.draw.line(pantalla, self.COLOR_HILO, pivot, bola, 3)
        pygame.draw.circle(pantalla, self.COLOR_HILO, pivot, 6)
        pygame.draw.circle(pantalla, self.COLOR_BOLA, bola, 25)
        pygame.draw.circle(pantalla, (240, 210, 90), bola, 25, 2)

        self._dibujar_etiqueta(pantalla, dx=0, dy=30, color=self.COLOR_HILO)


class Resorte(ObjetoLab):
    """
    Resorte colgado del techo con bloque en el extremo inferior.
    Ancla en (self.x, self.y).
    Movimiento: compresión/extensión vertical  ω = √(k/m).
    """

    COLOR_RESORTE = (150, 200, 150)
    COLOR_BLOQUE  = (180, 180, 220)
    ESPIRAS       = 12

    def __init__(self, x: float, y: float, masa: float = 1.0,
                 constante_k: float = 40.0, amplitud: float = 30.0):
        super().__init__(x, y, "Resorte (Ley de Hooke)")
        self.amplitud    = amplitud
        self._frecuencia = math.sqrt(constante_k / masa)
        self._offset_y   = 0.0

    def actualizar(self, dt: float) -> None:
        if not self.activo:
            return
        self.tiempo    += dt
        self._offset_y  = self.amplitud * math.sin(
                              self._frecuencia * self.tiempo)

    def dibujar(self, pantalla: pygame.Surface) -> None:
        if not self.activo:
            return
        ox = int(self.x)
        oy = int(self.y)

        long_base = 200                          # longitud en reposo
        long_real = long_base + int(self._offset_y)

        # Barra de anclaje en el techo
        pygame.draw.line(pantalla, (150, 150, 150),
                         (ox - 22, oy), (ox + 22, oy), 4)

        # Espiras (zigzag vertical)
        paso = long_real / self.ESPIRAS
        amp  = max(4, 14 - abs(int(self._offset_y)) // 10)
        for i in range(self.ESPIRAS):
            y1 = oy + int(i * paso)
            y2 = oy + int((i + 1) * paso)
            x1 = ox + (amp  if i % 2 == 0 else -amp)
            x2 = ox + (-amp if i % 2 == 0 else  amp)
            pygame.draw.line(pantalla, self.COLOR_RESORTE, (x1, y1), (x2, y2), 2)

        # Bloque colgante
        bloque_y = oy + long_real
        pygame.draw.rect(pantalla, self.COLOR_BLOQUE,
                         (ox - 20, bloque_y, 40, 24))
        pygame.draw.rect(pantalla, (200, 200, 240),
                         (ox - 20, bloque_y, 40, 24), 1)

        self._dibujar_etiqueta(pantalla, dx=0, dy=long_real + 30,
                               color=self.COLOR_RESORTE)