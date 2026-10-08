from jogo.config import *
from lib.Primitivas import bresenham, desenhar_poligono, desenhar_circulo, desenhar_elipse
from lib.Preenchimento import boundary_fill
from jogo.fonte import agendar_texto, largura_texto

BG, WHITE = (10, 10, 20), (255, 255, 255)
BR_X, BR_Y, BR_W, BR_H, BR_STEP = 59, 80, 60, 18, 66


class Abertura:

    def __init__(self, sup):
        self.sup = sup
        self.t = 0.0
        sup.set_clip(None)
        sup.fill(BG)
        self._desenhar_formas()

    def _desenhar_formas(self):
        s = self.sup
        cores = [(220, 60, 60), (240, 170, 40)]

        # tijolos: contorno com desenhar_poligono e interior com Boundary Fill
        for r in range(2):
            for c in range(8):
                x, y = BR_X + c * BR_STEP, BR_Y + r * 24
                desenhar_poligono(s, [(x, y), (x + BR_W, y), (x + BR_W, y + BR_H), (x, y + BR_H)], WHITE)
                boundary_fill(s, x + BR_W // 2, y + BR_H // 2, cores[r], WHITE)

        # retas: chão e trajetória
        bresenham(s, 40, 300, 600, 300, WHITE)
        bresenham(s, 346, 170, 420, 132, WHITE)

        # bola (circunferência) e raquete (elipse) com as primitivas
        desenhar_circulo(s, 320, 190, 28, (255, 140, 0))
        desenhar_elipse(s, 320, 260, 70, 12, (80, 150, 255))

    def update(self, dt):
        self.t += dt
        t = "BREAKOUT"
        agendar_texto((SCREEN_W - largura_texto(t, 8)) // 2, 14, t, WHITE, 8)
        if int(self.t * 2) % 2 == 0:                    # "PRESSIONE ENTER" pisca
            t = "PRESSIONE ENTER"
            agendar_texto((SCREEN_W - largura_texto(t, 3)) // 2, 340, t, WHITE, 3)
