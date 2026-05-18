"""
main.py — Punto de entrada del Simulador de Laboratorio Virtual
Simulador de Laboratorio Virtual - EdTech
Autor: Ortiz Cadena Maria Celeste Camila

REFACTORIZACIÓN APLICADA — Decompose Conditional:
El loop original tenía un if/elif sc==0/1/2/3 enorme.
Ahora usa un diccionario de escenas + polimorfismo:
    escena_actual.dibujar(pantalla)
    escena_actual.manejar_evento(evento)
"""

import pygame
import sys

from config import ANCHO_PANTALLA, ALTO_PANTALLA, FPS
from sesion_usuario import SesionUsuario
from escenas import EscenaQuimica, EscenaFisica
from escenas_ui import EscenaLogin, EscenaMenu


def construir_escenas(sesion: SesionUsuario) -> dict:
    """
    Instancia todas las escenas y las retorna en un diccionario.
    Agregar un nuevo laboratorio = añadir una entrada aquí.
    """
    escena_quimica = EscenaQuimica()
    escena_fisica  = EscenaFisica()

    return {
        "login":   EscenaLogin(sesion),
        "menu":    EscenaMenu(),
        "quimica": escena_quimica,
        "fisica":  escena_fisica,
    }


def main() -> None:
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("Simulador de Laboratorio Virtual")
    reloj_fps = pygame.time.Clock()

    sesion  = SesionUsuario()
    escenas = construir_escenas(sesion)
    nombre_escena_actual = "login"

    while True:
        escena_actual = escenas[nombre_escena_actual]

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            siguiente = escena_actual.manejar_evento(evento)
            if siguiente and siguiente in escenas:
                # Iniciar reloj si la escena destino es un laboratorio
                escena_destino = escenas[siguiente]
                if hasattr(escena_destino, "iniciar"):
                    escena_destino.iniciar()
                nombre_escena_actual = siguiente

        escena_actual.dibujar(pantalla)
        pygame.display.flip()
        reloj_fps.tick(FPS)


if __name__ == "__main__":
    main()