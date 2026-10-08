from jogo.config import *
from jogo.geometria import transladar, escalar

class Janela:
    def __init__(self):
        self.reset()

    def reset(self):
        self.xmin, self.ymin, self.xmax, self.ymax = 0, 0, WORLD_W, WORLD_H

    def tuple(self):
        return (self.xmin, self.ymin, self.xmax, self.ymax)

    @property
    def width(self): return self.xmax - self.xmin
    @property
    def zoom_level(self): return WORLD_W / self.width

    def center(self):
        return (self.xmin + self.xmax) / 2, (self.ymin + self.ymax) / 2

    def _corners(self):
        return [(self.xmin, self.ymin), (self.xmax, self.ymax)]

    def zoom(self, f):
        cx, cy = self.center()
        self._set(escalar(self._corners(), 1 / f, 1 / f, cx, cy))

    def pan(self, dx, dy):
        self._set(transladar(self._corners(), dx, dy))

    def center_on(self, x, y, k):
        cx, cy = self.center()
        self.pan((x - cx) * k, (y - cy) * k)

    def _set(self, corners):
        (ax, ay), (bx, by) = corners
        cx, cy = (ax + bx) / 2, (ay + by) / 2
        w = min(max(bx - ax, WORLD_W / MAX_ZOOM), WORLD_W)
        h = w * WORLD_H / WORLD_W
        x = min(max(cx - w / 2, 0), WORLD_W - w)
        y = min(max(cy - h / 2, 0), WORLD_H - h)
        self.xmin, self.ymin, self.xmax, self.ymax = x, y, x + w, y + h
