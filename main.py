import os
import pygame
from jogo.config import *
from jogo.renderizador import Renderizador
from jogo.abertura import Abertura
from jogo.menu import Menu
from jogo.fonte import desenhar_fila
from jogo.partida import Partida
from lib.Motor_grafico import setPixel


def carregar_textura(caminho):
    """Carrega a imagem da raquete; se não existir, gera uma textura listrada com setPixel."""
    if os.path.exists(caminho):
        return pygame.image.load(caminho).convert_alpha()
    tex = pygame.Surface((64, 32), pygame.SRCALPHA)
    for y in range(32):
        for x in range(64):
            c = (230, 230, 245) if ((x // 8) + (y // 8)) % 2 == 0 else (90, 110, 200)
            setPixel(tex, x, y, (*c, 255))
    return tex


def main():
    pygame.init()
    tela = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Breakout - Computação Gráfica")
    clock = pygame.time.Clock()

    sup = pygame.Surface((SCREEN_W, SCREEN_H))       # "framebuffer"
    rend = Renderizador(sup, carregar_textura("assets/paddle.png"))
    abertura, menu, jogo = Abertura(sup), Menu(sup), None
    estado, rodando = "intro", True

    while rodando:
        dt = min(clock.tick(FPS) / 1000.0, 0.1)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                rodando = False
            elif estado == "intro":
                if ev.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    estado = "menu"
            elif estado == "menu":
                acao = menu.handle(ev)
                if acao == "play":
                    jogo, estado = Partida(menu.speed), "game"
                elif acao == "quit":
                    rodando = False
            elif estado == "game" and ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    estado = "menu"
                else:
                    jogo.keydown(ev.key)

        sup.lock()
        if estado == "intro":
            abertura.update(dt)
        elif estado == "menu":
            menu.update(dt)
            menu.draw()
        elif estado == "game":
            jogo.update(dt, pygame.key.get_pressed())
            rend.desenhar_jogo(jogo)
        sup.unlock()

        tela.blit(sup, (0, 0))
        desenhar_fila(tela)                  # textos: render + blit direto na tela
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
