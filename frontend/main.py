"""
main.py — Punto de entrada del Simulador de Laboratorio Virtual
Autor: Ortiz Cadena Maria Celeste Camila

ACTUALIZACIÓN: Se agrega dt (delta time) real para animar
los objetos de ObjetoLab de forma fluida e independiente del FPS.
"""

import pygame
import sys

from config import ANCHO_PANTALLA, ALTO_PANTALLA, FPS
from sesion_usuario import SesionUsuario
from escenas import EscenaQuimica, EscenaFisica
from escenas_ui import EscenaLogin, EscenaMenu


def construir_escenas(sesion: SesionUsuario) -> dict:
    return {
        "login":   EscenaLogin(sesion),
        "menu":    EscenaMenu(),
        "quimica": EscenaQuimica(),
        "fisica":  EscenaFisica(),
    }


def main() -> None:
    pygame.init()
    pantalla   = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("Simulador de Laboratorio Virtual")
    reloj_fps  = pygame.time.Clock()

    sesion   = SesionUsuario()
    escenas  = construir_escenas(sesion)
    escena_actual_nombre = "login"

    while True:
        # dt en segundos — independiente del FPS
        dt = reloj_fps.tick(FPS) / 1000.0
        escena = escenas[escena_actual_nombre]

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            siguiente = escena.manejar_evento(evento)
            if siguiente and siguiente in escenas:
                destino = escenas[siguiente]
                if hasattr(destino, "iniciar"):
                    destino.iniciar()
                escena_actual_nombre = siguiente

        # Actualizar objetos animados (solo labs lo implementan)
        escena.actualizar(dt)

        escena.dibujar(pantalla)
        pygame.display.flip()


if __name__ == "__main__":
    main()
    