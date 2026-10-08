import math
from jogo.config import *
from jogo.geometria import transladar, escalar, rotacionar

_N = 12
_UNIT_CIRCLE = [(math.cos(2 * math.pi * i / _N), math.sin(2 * math.pi * i / _N)) for i in range(_N)]
# gradiente vertical simples: vértices de cima claros, vértices de baixo escuros
_TOPO, _BASE = (255, 235, 170), (210, 90, 10)
_BALL_COLORS = []
for _x, _y in _UNIT_CIRCLE:
    _t = (_y + 1) / 2                       # 0 no topo (y = -1) ... 1 embaixo (y = +1)
    _BALL_COLORS.append(tuple(int(_TOPO[k] + (_BASE[k] - _TOPO[k]) * _t) for k in range(3)))
DEATH_TIME = 0.3


class Paddle:
    UNIT = [(-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5)]
    UVS = [(0, 0), (1, 0), (1, 1), (0, 1)]

    def __init__(self):
        self.x, self.y, self.h = WORLD_W / 2, PADDLE_Y, PADDLE_H
        self.sx = 1.0
        self.uvs = Paddle.UVS

    @property
    def width(self): return PADDLE_W * self.sx
    @property
    def left(self): return self.x - self.width / 2
    @property
    def top(self): return self.y - self.h / 2

    def move(self, dx):
        half = self.width / 2
        self.x = min(max(self.x + dx, half), WORLD_W - half)

    def polygon(self):
        pts = escalar(Paddle.UNIT, self.width, self.h, 0, 0)
        return transladar(pts, self.x, self.y)


class Ball:
    def __init__(self):
        self.r = BALL_R
        self.x = self.y = self.vx = self.vy = 0.0

    def polygon(self):
        pts = escalar(_UNIT_CIRCLE, self.r, self.r, 0, 0)
        return transladar(pts, self.x, self.y)

    def vertex_colors(self):
        return _BALL_COLORS


class Brick:
    def __init__(self, row, col):
        self.row, self.col = row, col
        self.x = BRICK_LEFT + col * (BRICK_W + BRICK_GAP)
        self.y = BRICK_TOP + row * (BRICK_H + BRICK_GAP)
        self.light, self.dark = ROW_COLORS[row % len(ROW_COLORS)]
        self.alive, self.gone, self.t = True, False, 0.0

    def hit(self):
        self.alive = False

    def update(self, dt):
        if not self.alive:
            self.t += dt
            if self.t >= DEATH_TIME:
                self.gone = True

    def polygon(self):
        hw, hh = BRICK_W / 2, BRICK_H / 2
        pts = [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]
        if not self.alive:
            k = self.t / DEATH_TIME
            f = max(0.05, 1 - k)
            pts = escalar(pts, f, f, 0, 0)
            pts = rotacionar(pts, k * 180, 0, 0)
        return transladar(pts, self.x + hw, self.y + hh)

    def vertex_colors(self):
        return [self.light, self.light, self.dark, self.dark]
