"""
PROTOTIPO BASE - SIN REFACTORIZAR
Simulador de Laboratorio Virtual - Plataforma EdTech
Autor: Ortiz Cadena Maria Celeste Camila
NOTA: Este código es el punto de partida ANTES de aplicar refactorización.
Contiene problemas intencionales que se corregirán en la siguiente etapa.
"""

import pygame
import sys
import time

#  PROBLEMA 1: Números mágicos dispersos por todo el código (Magic Numbers)
#  PROBLEMA 2: Lógica mezclada, sin separación de responsabilidades
#  PROBLEMA 3: Código duplicado en las escenas
#  PROBLEMA 4: Variables con nombres poco descriptivos (n, t, c, etc.)

pygame.init()

p = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Lab Virtual")

#  Variables con nombres sin sentido
r = True
t = 0
n = ""
pw = ""
log = False
sc = 0  # 0=login, 1=menu, 2=quimica, 3=fisica

f1 = pygame.font.SysFont("arial", 32)
f2 = pygame.font.SysFont("arial", 20)
f3 = pygame.font.SysFont("arial", 16)

#  Colores hardcodeados repetidos por todo el código sin nombres
BG = (15, 15, 40)
W = (255, 255, 255)
G = (100, 200, 100)
BL = (50, 100, 200)
R = (200, 50, 50)
GR = (150, 150, 150)

#  PROBLEMA: Datos de usuario hardcodeados directamente
usuarios = {"estudiante": "1234", "admin": "admin123"}

#  Variables globales mezcladas con lógica de negocio
tiempo_inicio = 0
tiempo_limite = 300  #  Magic number: 5 minutos en segundos
elementos_quimica = []
elementos_fisica = []
reacciones = []
input_activo = ""

# ---- FUNCIONES SIN ESTRUCTURA (todo en global) ----

def dibujar_login():
    # Función muy larga que hace demasiadas cosas a la vez
    global n, pw, log, sc, input_activo
    p.fill((15, 15, 40))
    
    # Título
    txt = f1.render("LABORATORIO VIRTUAL", True, (255, 255, 255))
    p.blit(txt, (640 - txt.get_width()//2, 80))
    
    txt2 = f2.render("Iniciar Sesion", True, (200, 200, 200))
    p.blit(txt2, (640 - txt2.get_width()//2, 150))
    
    # Caja usuario
    pygame.draw.rect(p, (50, 50, 80), (440, 230, 400, 45), border_radius=8)
    if input_activo == "user":
        pygame.draw.rect(p, (100, 150, 255), (440, 230, 400, 45), 2, border_radius=8)
    else:
        pygame.draw.rect(p, (80, 80, 120), (440, 230, 400, 45), 2, border_radius=8)
    label_u = f3.render("Usuario", True, (180, 180, 200))
    p.blit(label_u, (444, 215))
    txt_n = f2.render(n, True, (255, 255, 255))
    p.blit(txt_n, (452, 243))
    
    # Caja contraseña
    pygame.draw.rect(p, (50, 50, 80), (440, 310, 400, 45), border_radius=8)
    if input_activo == "pass":
        pygame.draw.rect(p, (100, 150, 255), (440, 310, 400, 45), 2, border_radius=8)
    else:
        pygame.draw.rect(p, (80, 80, 120), (440, 310, 400, 45), 2, border_radius=8)
    label_p = f3.render("Contrasena", True, (180, 180, 200))
    p.blit(label_p, (444, 295))
    pw_mask = "*" * len(pw)
    txt_pw = f2.render(pw_mask, True, (255, 255, 255))
    p.blit(txt_pw, (452, 323))
    
    # Botón
    pygame.draw.rect(p, (50, 100, 200), (540, 390, 200, 50), border_radius=10)
    btn_txt = f2.render("ENTRAR", True, (255, 255, 255))
    p.blit(btn_txt, (640 - btn_txt.get_width()//2, 405))
    
    # Mensaje error
    if hasattr(dibujar_login, 'error') and dibujar_login.error:
        err = f3.render("Usuario o contrasena incorrectos", True, (255, 100, 100))
        p.blit(err, (640 - err.get_width()//2, 460))


def dibujar_menu():
    # Otro bloque largo sin estructura
    global sc
    p.fill((15, 15, 40))
    
    titulo = f1.render("SELECCIONA TU LABORATORIO", True, (255, 255, 255))
    p.blit(titulo, (640 - titulo.get_width()//2, 80))
    
    # Botón química -  coordenadas mágicas
    pygame.draw.rect(p, (30, 100, 60), (200, 250, 380, 180), border_radius=15)
    pygame.draw.rect(p, (50, 180, 100), (200, 250, 380, 180), 3, border_radius=15)
    q_txt = f1.render("QUIMICA", True, (255, 255, 255))
    p.blit(q_txt, (390 - q_txt.get_width()//2, 320))
    q_sub = f3.render("Reacciones y compuestos", True, (180, 255, 180))
    p.blit(q_sub, (390 - q_sub.get_width()//2, 370))
    
    # Botón física -  código casi idéntico al de química (duplicado)
    pygame.draw.rect(p, (30, 60, 120), (700, 250, 380, 180), border_radius=15)
    pygame.draw.rect(p, (50, 100, 220), (700, 250, 380, 180), 3, border_radius=15)
    f_txt = f1.render("FISICA", True, (255, 255, 255))
    p.blit(f_txt, (890 - f_txt.get_width()//2, 320))
    f_sub = f3.render("Movimiento y fuerzas", True, (180, 180, 255))
    p.blit(f_sub, (890 - f_sub.get_width()//2, 370))


def dibujar_quimica():
    #  Función enorme que dibuja TODO sin separar responsabilidades
    global t, sc
    p.fill((10, 20, 35))
    
    # Header
    pygame.draw.rect(p, (20, 40, 70), (0, 0, 1280, 70))
    h_txt = f2.render("LABORATORIO DE QUIMICA", True, (255, 255, 255))
    p.blit(h_txt, (20, 22))
    
    #  Reloj calculado directamente aquí sin encapsularlo
    elapsed = time.time() - tiempo_inicio
    remaining = 300 - elapsed  #  Magic number 300
    if remaining < 0:
        remaining = 0
    mins = int(remaining // 60)
    secs = int(remaining % 60)
    clock_str = f"Tiempo: {mins:02d}:{secs:02d}"
    c_txt = f2.render(clock_str, True, (255, 220, 100) if remaining > 60 else (255, 80, 80))  #  Magic number 60
    p.blit(c_txt, (1100, 22))
    
    # Mesa de laboratorio
    pygame.draw.rect(p, (60, 40, 20), (100, 450, 1080, 30))
    pygame.draw.rect(p, (80, 55, 25), (100, 480, 1080, 15))
    
    # Elementos de química en la mesa
    # Vaso de precipitados
    pygame.draw.rect(p, (200, 230, 255), (200, 350, 60, 100), 3)
    pygame.draw.rect(p, (150, 200, 255, 100), (203, 380, 54, 67))
    vaso_txt = f3.render("H2O", True, (150, 200, 255))
    p.blit(vaso_txt, (215, 460))
    
    # Tubo de ensayo
    pygame.draw.ellipse(p, (200, 150, 255), (400, 340, 40, 15))
    pygame.draw.rect(p, (200, 150, 255), (402, 347, 36, 90), 3)
    pygame.draw.ellipse(p, (200, 150, 255), (402, 427, 36, 20))
    tubo_txt = f3.render("NaCl", True, (200, 150, 255))
    p.blit(tubo_txt, (395, 460))
    
    # Botón volver
    pygame.draw.rect(p, (80, 30, 30), (20, 620, 130, 40), border_radius=8)
    back = f3.render("< VOLVER", True, (255, 200, 200))
    p.blit(back, (35, 632))


def dibujar_fisica():
    #  Prácticamente el mismo esqueleto que dibujar_quimica() — código duplicado
    global t, sc
    p.fill((10, 15, 30))
    
    pygame.draw.rect(p, (20, 30, 60), (0, 0, 1280, 70))
    h_txt = f2.render("LABORATORIO DE FISICA", True, (255, 255, 255))
    p.blit(h_txt, (20, 22))
    
    #  Mismo reloj copiado y pegado
    elapsed = time.time() - tiempo_inicio
    remaining = 600 - elapsed  #  Otro magic number diferente: 10 minutos
    if remaining < 0:
        remaining = 0
    mins = int(remaining // 60)
    secs = int(remaining % 60)
    clock_str = f"Tiempo: {mins:02d}:{secs:02d}"
    c_txt = f2.render(clock_str, True, (255, 220, 100) if remaining > 60 else (255, 80, 80))
    p.blit(c_txt, (1100, 22))
    
    # Mesa
    pygame.draw.rect(p, (50, 50, 60), (100, 450, 1080, 30))
    
    # Péndulo (dibujado a mano sin estructura)
    pygame.draw.line(p, (200, 200, 200), (640, 150), (640, 350), 3)
    pygame.draw.circle(p, (220, 180, 50), (640, 360), 25)
    pendulo_txt = f3.render("Pendulo Simple", True, (200, 200, 200))
    p.blit(pendulo_txt, (600, 395))
    
    # Resorte
    for i in range(10):
        y = 280 + i * 15
        pygame.draw.line(p, (150, 200, 150), (300 + (i%2)*30, y), (330 - (i%2)*30, y+15), 2)
    resorte_txt = f3.render("Resorte", True, (150, 200, 150))
    p.blit(resorte_txt, (295, 460))
    
    pygame.draw.rect(p, (80, 30, 30), (20, 620, 130, 40), border_radius=8)
    back = f3.render("< VOLVER", True, (255, 200, 200))
    p.blit(back, (35, 632))


# ---- LOOP PRINCIPAL ---- (todo mezclado)
dibujar_login.error = False

while r:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            r = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            
            if sc == 0:  # Login
                if 440 <= mx <= 840 and 230 <= my <= 275:
                    input_activo = "user"
                elif 440 <= mx <= 840 and 310 <= my <= 355:
                    input_activo = "pass"
                elif 540 <= mx <= 740 and 390 <= my <= 440:
                    #  Validación directa en el loop
                    if n in usuarios and usuarios[n] == pw:
                        log = True
                        sc = 1
                        dibujar_login.error = False
                    else:
                        dibujar_login.error = True
            
            elif sc == 1:  # Menú
                if 200 <= mx <= 580 and 250 <= my <= 430:
                    sc = 2
                    tiempo_inicio = time.time()
                elif 700 <= mx <= 1080 and 250 <= my <= 430:
                    sc = 3
                    tiempo_inicio = time.time()
            
            elif sc in [2, 3]:  # Labs
                if 20 <= mx <= 150 and 620 <= my <= 660:
                    sc = 1
        
        if event.type == pygame.KEYDOWN:
            if sc == 0:
                if event.key == pygame.K_BACKSPACE:
                    if input_activo == "user":
                        n = n[:-1]
                    elif input_activo == "pass":
                        pw = pw[:-1]
                elif event.key == pygame.K_TAB:
                    input_activo = "pass" if input_activo == "user" else "user"
                else:
                    if input_activo == "user" and len(n) < 20:
                        n += event.unicode
                    elif input_activo == "pass" and len(pw) < 20:
                        pw += event.unicode
    
    #  Condicional enorme sin estructura
    if sc == 0:
        dibujar_login()
    elif sc == 1:
        dibujar_menu()
    elif sc == 2:
        dibujar_quimica()
    elif sc == 3:
        dibujar_fisica()
    
    pygame.display.flip()
    pygame.time.Clock().tick(60)  #  Magic number 60 (FPS)

pygame.quit()
sys.exit()