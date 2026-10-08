from jogo.config import *
from lib.Primitivas import bresenham, desenhar_poligono
from lib.Preenchimento import boundary_fill
from lib.Contornos import contorno_circulo, contorno_elipse
from jogo.fonte import agendar_texto, largura_texto

BG, WHITE = (10, 10, 20), (255, 255, 255)
BR_X, BR_Y, BR_W, BR_H, BR_STEP = 59, 80, 60, 18, 66


class Abertura:
    def __init__(self, sup):
        self.sup = sup
        self.t, self.stage = 0.0, 0
        self.stages = [self._titulo, self._retas, self._circulo, self._elipse, self._preenchimentos]
        self.titulo = False
        sup.set_clip(None)
        sup.fill(BG)

    def _titulo(self):
        self.titulo = True

    def _retas(self):
        for r in range(2):
            for c in range(8):
                x, y = BR_X + c * BR_STEP, BR_Y + r * 24
                desenhar_poligono(self.sup, [(x, y), (x + BR_W, y), (x + BR_W, y + BR_H), (x, y + BR_H)], WHITE)
        bresenham(self.sup, 40, 300, 600, 300, WHITE)
        bresenham(self.sup, 346, 170, 420, 132, WHITE)

    def _circulo(self):
        contorno_circulo(self.sup, 320, 190, 28, WHITE)

    def _elipse(self):
        contorno_elipse(self.sup, 320, 260, 70, 12, WHITE)

    def _preenchimentos(self):
        s = self.sup
        cores = [(220, 60, 60), (240, 170, 40)]
        for r in range(2):
            for c in range(8):
                boundary_fill(s, BR_X + c * BR_STEP + BR_W // 2, BR_Y + r * 24 + BR_H // 2, cores[r], WHITE)
        boundary_fill(s, 320, 190, (255, 140, 0), WHITE)
        boundary_fill(s, 320, 260, (80, 150, 255), WHITE)

    @property
    def done(self):
        return self.stage >= len(self.stages)

    def update(self, dt):
        self.t += dt
        if not self.done and self.t >= self.stage * 0.6:
            self.stages[self.stage]()
            self.stage += 1
        if self.titulo:
            t = "BREAKOUT"
            agendar_texto((SCREEN_W - largura_texto(t, 8)) // 2, 14, t, WHITE, 8)
        if self.done and int(self.t * 2) % 2 == 0:      # pisca
            t = "PRESSIONE ENTER"
            agendar_texto((SCREEN_W - largura_texto(t, 3)) // 2, 340, t, WHITE, 3)
