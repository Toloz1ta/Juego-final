import pygame
import sys
import random
import os

pygame.init()

# Configuración de la pantalla
ancho, alto = 1920, 1080
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("DinoRun 🦖")

fps = pygame.time.Clock()
fuente = pygame.font.SysFont("arial", 24)
fuente_grande = pygame.font.SysFont("arial", 60)

# Colores
cielo = (130, 200, 229)
color = (53, 56, 57)
blanco = (255, 255, 255)
rojo = (200, 0, 0)

# Cargar imágenes
dino = pygame.image.load("sprites/Dinosaurio.png")
cactus = pygame.image.load("sprites/cactus.png")
pajaro = pygame.image.load("sprites/pajaro.png")
roca = pygame.image.load("sprites/roca.png")
suelo = pygame.image.load("sprites/suelo.png")

# Cambiar tamaño de las imágenes
dino = pygame.transform.scale(dino, (150, 150))
cactus = pygame.transform.scale(cactus, (80, 110))
pajaro = pygame.transform.scale(pajaro, (100, 65))
roca = pygame.transform.scale(roca, (70, 70))

# Medidas del suelo
suelo_ancho = suelo.get_width()
suelo = pygame.transform.scale(
    suelo, (suelo_ancho, suelo.get_height()))

suelo_x1 = 0
suelo_x2 = suelo_ancho
suelo_y = 800

# Dinosaurio
dino_rect = pygame.Rect(100, 650, 100, 100)
velocidad_x = 7

# Salto
velocidad_y = 0
gravedad = 0.8
fuerza_salto = -18
en_el_suelo = True

# Velocidad y puntuación
velocidad_obstaculos = 6
puntos = 0

# Obstáculos
cactus_rect = cactus.get_rect(midbottom=(ancho + 300, suelo_y))
pajaro_rect = pajaro.get_rect(midbottom=(ancho + 900, suelo_y))
roca_rect = roca.get_rect(midtop=(random.randint(200, ancho - 70), -70))

# Estado del juego
game_over = False
tiempo_puntos = 0


def reiniciar_juego():
    global dino_rect, velocidad_x, velocidad_y, en_el_suelo
    global cactus_rect, pajaro_rect, roca_rect
    global velocidad_obstaculos, puntos, game_over
    global suelo_x1, suelo_x2, tiempo_puntos

    dino_rect = pygame.Rect(100, 650, 100, 100)

    velocidad_y = 0
    en_el_suelo = True

    cactus_rect = cactus.get_rect(midbottom=(ancho + 300, suelo_y))
    pajaro_rect = pajaro.get_rect(midbottom=(ancho + 900, suelo_y))
    roca_rect = roca.get_rect(
        midtop=(random.randint(200, ancho - 70), -70)
    )

    velocidad_obstaculos = 6
    puntos = 0
    game_over = False
    tiempo_puntos = 0

    suelo_x1 = 0
    suelo_x2 = suelo_ancho


# Bucle principal
while True:

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if evento.key == pygame.K_r and game_over:
                reiniciar_juego()

    teclas = pygame.key.get_pressed()

    if not game_over:

        # Movimiento horizontal del dinosaurio
        if teclas[pygame.K_LEFT]:
            dino_rect.x -= velocidad_x

        if teclas[pygame.K_RIGHT]:
            dino_rect.x += velocidad_x

        # Evitar que el dinosaurio salga de la pantalla
        if dino_rect.left < 0:
            dino_rect.left = 0

        if dino_rect.right > ancho:
            dino_rect.right = ancho

        # Salto del dinosaurio
        if (
            teclas[pygame.K_SPACE] or teclas[pygame.K_UP]
        ) and en_el_suelo:
            velocidad_y = fuerza_salto
            en_el_suelo = False

        # Física del salto
        dino_rect.y += int(velocidad_y)
        velocidad_y += gravedad

        if dino_rect.bottom >= 750:
            dino_rect.bottom = 750
            velocidad_y = 0
            en_el_suelo = True

        # Mover el suelo continuamente
        suelo_x1 -= velocidad_obstaculos
        suelo_x2 -= velocidad_obstaculos

        if suelo_x1 + suelo_ancho <= 0:
            suelo_x1 = suelo_x2 + suelo_ancho

        if suelo_x2 + suelo_ancho <= 0:
            suelo_x2 = suelo_x1 + suelo_ancho

        # Mover obstáculos
        cactus_rect.x -= velocidad_obstaculos
        pajaro_rect.x -= velocidad_obstaculos

        # La roca cae verticalmente
        roca_rect.y += velocidad_obstaculos

        # Reaparecer cactus
        if cactus_rect.right < 0:
            cactus_rect.left = ancho + random.randint(200, 600)
            puntos += 1

        # Reaparecer pájaro
        if pajaro_rect.right < 0:
            pajaro_rect.left = ancho + random.randint(400, 900)
            puntos += 1

        # Reaparecer roca desde arriba en una posición aleatoria
        if roca_rect.top > alto:
            roca_rect.x = random.randint(200, ancho - roca_rect.width)
            roca_rect.y = -roca_rect.height
            puntos += 1

        # Aumentar dificultad cada 10 puntos
        if puntos > 0 and puntos % 10 == 0:
            velocidad_obstaculos = min(6 + puntos // 10, 18)

        # Detectar colisiones
        if (
            dino_rect.colliderect(cactus_rect)
            or dino_rect.colliderect(pajaro_rect)
            or dino_rect.colliderect(roca_rect)
        ):
            game_over = True

    # Dibujar el fondo
    pantalla.fill(cielo)

    # Dibujar el suelo
    pantalla.blit(suelo, (suelo_x1, suelo_y))
    pantalla.blit(suelo, (suelo_x2, suelo_y))

    # Dibujar obstáculos y dinosaurio
    pantalla.blit(dino, dino_rect)
    pantalla.blit(cactus, cactus_rect)
    pantalla.blit(pajaro, pajaro_rect)
    pantalla.blit(roca, roca_rect)

    # Mostrar puntuación
    texto_puntos = fuente.render(
        f"Puntos: {puntos}", True, color
    )
    pantalla.blit(texto_puntos, (30, 30))

    # Pantalla de Game Over
    if game_over:
        texto_fin = fuente_grande.render(
            "GAME OVER", True, rojo
        )
        texto_reiniciar = fuente.render(
            "Presiona R para reiniciar", True, color
        )

        pantalla.blit(
            texto_fin,
            texto_fin.get_rect(center=(ancho // 2, alto // 2 - 40))
        )
        pantalla.blit(
            texto_reiniciar,
            texto_reiniciar.get_rect(
                center=(ancho // 2, alto // 2 + 30)
            )
        )

    pygame.display.flip()
    fps.tick(60)
