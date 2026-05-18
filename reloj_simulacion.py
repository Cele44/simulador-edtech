"""
COMPONENTE 2: RelojSimulacion
Simulador de Laboratorio Virtual - EdTech
Autor: Ortiz Cadena Maria Celeste Camila

RESPONSABILIDAD: Controlar el tiempo de duración de una práctica de laboratorio.
REUTILIZABLE EN: Todos los laboratorios (se instancia con duración diferente).

REFACTORIZACIÓN APLICADA:
  - Extract Method: El cálculo de tiempo restante y el formateo
    mm:ss se extrajeron del dibujar_quimica() y dibujar_fisica()
    donde estaban duplicados, a métodos propios de esta clase.
  - Replace Magic Number: 300, 600, 60 reemplazados por constantes
    importadas de config.py (TIEMPO_LAB_QUIMICA, UMBRAL_ALERTA, etc.)
"""

import time
from config import UMBRAL_ALERTA, COLOR_RELOJ_NORMAL, COLOR_RELOJ_ALERTA


class RelojSimulacion:
    """
    Temporizador configurable para prácticas de laboratorio.
    Cada laboratorio recibe su propio tiempo límite al instanciarlo.

    Ejemplo de uso:
        reloj_quimica = RelojSimulacion(duracion=TIEMPO_LAB_QUIMICA)
        reloj_quimica.iniciar()
        ...
        texto, color = reloj_quimica.formato_display()
    """

    def __init__(self, duracion: int, umbral_alerta: int = UMBRAL_ALERTA):
        """
        Parámetros
        ----------
        duracion      : tiempo total de la práctica en segundos
        umbral_alerta : segundos restantes a partir de los cuales
                        el reloj cambia de color para alertar al estudiante
        """
        self.duracion_total: int   = duracion
        self.umbral_alerta: int    = umbral_alerta
        self._tiempo_inicio: float = 0.0
        self._activo: bool         = False

    # ── Control del reloj ─────────────────────────────────

    def iniciar(self) -> None:
        """Arranca el temporizador desde el momento actual."""
        self._tiempo_inicio = time.time()
        self._activo = True

    def pausar(self) -> None:
        """Detiene el conteo (para futuras extensiones)."""
        self._activo = False

    def reiniciar(self) -> None:
        """Resetea y vuelve a arrancar el reloj."""
        self.iniciar()

    # ── Cálculos de tiempo ────────────────────────────────

    def segundos_restantes(self) -> float:
        """
        Retorna los segundos que quedan en la práctica.

        REFACTORIZACIÓN — Extract Method:
        En el prototipo este cálculo estaba inline dentro de
        dibujar_quimica() y dibujar_fisica(), duplicado en ambas.
        """
        if not self._activo:
            return float(self.duracion_total)
        transcurridos = time.time() - self._tiempo_inicio
        restantes = self.duracion_total - transcurridos
        return max(0.0, restantes)

    def esta_vencido(self) -> bool:
        """Indica si el tiempo de la práctica se agotó."""
        return self.segundos_restantes() <= 0

    def en_zona_alerta(self) -> bool:
        """True cuando el tiempo restante cae bajo el umbral de alerta."""
        return self.segundos_restantes() <= self.umbral_alerta

    def porcentaje_restante(self) -> float:
        """Devuelve un valor entre 0.0 y 1.0 para barras de progreso."""
        return self.segundos_restantes() / self.duracion_total

    # ── Formato para pantalla ─────────────────────────────

    def formato_mm_ss(self) -> str:
        """
        Formatea los segundos restantes como 'MM:SS'.

        REFACTORIZACIÓN — Extract Method:
        El formateo estaba duplicado en cada función de dibujo;
        ahora reside en un único lugar.
        """
        segundos = int(self.segundos_restantes())
        minutos  = segundos // 60
        segs     = segundos % 60
        return f"{minutos:02d}:{segs:02d}"

    def formato_display(self) -> tuple[str, tuple]:
        """
        Retorna (texto_reloj, color_pygame) listo para renderizar.
        El color cambia automáticamente según el umbral de alerta.
        """
        texto = f"Tiempo: {self.formato_mm_ss()}"
        color = COLOR_RELOJ_ALERTA if self.en_zona_alerta() else COLOR_RELOJ_NORMAL
        return texto, color

    def __repr__(self) -> str:
        return (
            f"RelojSimulacion(duracion={self.duracion_total}s, "
            f"restante={self.formato_mm_ss()}, "
            f"activo={self._activo})"
        )