import pygame
from lib.Primitivas import *
from lib.Preenchimento import *
from poligonos.Prancha import *
from poligonos.Bola import *
from core.game import *
WIDTH,HEIGHT = 640,480

WHITE = (255,255,255)
DARKBLUE = (36,90,190)
LIGHTBLUE = (0,176,240)
RED = (255,0,0)
ORANGE = (255,100,0)
YELLOW = (255,255,0)

score = 0
lives = 3
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Breakout')
clock = pygame.time.Clock()
prancha = Prancha((255,255,255),50,10,WIDTH//2,HEIGHT//1.2)
bola = Bola((255,255,255),10,WIDTH//2,HEIGHT//2)
tijolos = []
running = True
gerar_tijolos(screen,tijolos,45,10,(50,50,50))
font = pygame.font.Font(None, 34)
text_score = font.render("Score: " + str(score), 1, WHITE)
text_lives = font.render("Lives: " + str(lives), 1, WHITE)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 95, 195))
    screen.blit(text_score, (20,10))
    screen.blit(text_lives, (150,10))
    atualizar_objetos(screen,bola,prancha,tijolos)
    pygame.display.flip()
    clock.tick(120)
pygame.quit()
