import math
import pygame
from jogo.config import *
from lib.Preenchimento import scanline_fill_gradiente
from jogo.geometria import escalar
from jogo.fonte import agendar_texto, largura_texto

BG, WHITE = (10, 10, 20), (255, 255, 255)
SEL = [(255, 180, 70), (255, 180, 70), (190, 70, 10), (190, 70, 10)]
IDLE = [(70, 80, 140), (70, 80, 140), (25, 30, 70), (25, 30, 70)]


class Menu:
    DIFFS = [("FÁCIL", 0.8), ("NORMAL", 1.0), ("DIFÍCIL", 1.3)]

    def __init__(self, sup):
        self.sup = sup
        self.sel, self.diff, self.t = 0, 1, 0.0
        self.rects = [(170, 150 + i * 60, 470, 194 + i * 60) for i in range(3)]

    @property
    def speed(self):
        return Menu.DIFFS[self.diff][1]

    def label(self, i):
        return ["JOGAR", "DIFICULDADE " + Menu.DIFFS[self.diff][0], "SAIR"][i]

    def update(self, dt):
        self.t += dt

    def _activate(self):
        if self.sel == 0:
            return "play"
        if self.sel == 2:
            return "quit"
        self.diff = (self.diff + 1) % len(Menu.DIFFS)
        return None

    def handle(self, ev):
        if ev.type == pygame.KEYDOWN:
            if ev.key in (pygame.K_UP, pygame.K_w):
                self.sel = (self.sel - 1) % 3
            elif ev.key in (pygame.K_DOWN, pygame.K_s):
                self.sel = (self.sel + 1) % 3
            elif ev.key in (pygame.K_LEFT, pygame.K_RIGHT) and self.sel == 1:
                step = 1 if ev.key == pygame.K_RIGHT else -1
                self.diff = (self.diff + step) % len(Menu.DIFFS)
            elif ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self._activate()
        elif ev.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
            mx, my = ev.pos
            for i, (x0, y0, x1, y1) in enumerate(self.rects):
                if x0 <= mx <= x1 and y0 <= my <= y1:
                    self.sel = i
                    if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                        return self._activate()
        return None

    def draw(self):
        sup = self.sup
        sup.set_clip(None)
        sup.fill(BG)
        t = "BREAKOUT"
        agendar_texto((SCREEN_W - largura_texto(t, 6)) // 2, 50, t, WHITE, 6)
        for i, (x0, y0, x1, y1) in enumerate(self.rects):
            pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
            if i == self.sel:
                k = 1 + 0.04 * math.sin(self.t * 6)
                pts = escalar(pts, k, k, (x0 + x1) / 2, (y0 + y1) / 2)
            scanline_fill_gradiente(sup, pts, SEL if i == self.sel else IDLE)
            txt = self.label(i)
            agendar_texto((x0 + x1 - largura_texto(txt, 3)) // 2, y0 + 14, txt, WHITE, 3)
