
import pygame
import sys
import random
import os

pygame.init()

ancho, alto = 1920, 1080
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("DinoRun 🦖")
fps = pygame.time.Clock()
fuente = pygame.font.SysFont("arial", 24)

cielo = (130, 200, 229)
dino = pygame.image.load("sprites/Dinosaurio.png")

cactus = pygame.image.load("sprites/cactus.png")
pajaro = pygame.image.load("sprites/pajaro.png")
roca = pygame.image.load("sprites/roca.png")

velocidad_obstaculos = 6

suelo = pygame.image.load("sprites/suelo.png")
color = (53, 56, 57)
puntos = 0

dino_rect = pygame.Rect(100, 650, 100, 100)
dino = pygame.transform.scale(dino, (150, 150))

suelo_y = 750
velocidad_y = 0
gravedad = 0.8
fuerza_salto = -15
en_el_suelo = True

# Obstáculos
roca_x = random.randint(0, ancho)
roca_y = 0

jugando = True

while jugando:
    fps.tick(60)
    pantalla.fill(cielo)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT]:
        dino_rect.x -= 5

    if teclas[pygame.K_RIGHT]:
        dino_rect.x += 5

    if (teclas[pygame.K_SPACE] or teclas[pygame.K_UP]) and en_el_suelo:
        velocidad_y = fuerza_salto
        en_el_suelo = False

    # Movimiento vertical del dinosaurio
    dino_rect.y += velocidad_y
    velocidad_y += gravedad

    if dino_rect.bottom >= suelo_y:
        velocidad_y = 0
        en_el_suelo = True
        dino_rect.bottom = suelo_y

    # Caída de la roca
    roca_y += velocidad_obstaculos

    # Dibujar elementos
    pantalla.blit(dino, dino_rect)
    pantalla.blit(suelo, (0, 800))
    pantalla.blit(suelo, (700, 800))
    pantalla.blit(roca, (roca_x, roca_y))

    pygame.display.flip()

pygame.quit()
sys.exit()
