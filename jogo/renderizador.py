import pygame
from jogo.config import *
from lib.Primitivas import bresenham
from lib.Preenchimento import scanline_fill, scanline_fill_gradiente, scanline_texture
from lib.Recorte import cohen_sutherland
from lib.Viewport import janela_viewport
from jogo.geometria import aplica_transformacao
from jogo.fonte import agendar_texto, largura_texto

WHITE = (255, 255, 255)


def retangulo_pts(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def limpar(sup, cor, vp=None):
    """Limpa a tela ou uma viewport (única chamada que não é set pixel)."""
    if vp is None:
        sup.fill(cor)
    else:
        x0, y0, x1, y1 = vp
        sup.fill(cor, pygame.Rect(x0, y0, x1 - x0 + 1, y1 - y0 + 1))


def clip_viewport(sup, vp):
    """Scissor da viewport: o setPixel (set_at) respeita o clip da superfície."""
    if vp is None:
        sup.set_clip(None)
    else:
        x0, y0, x1, y1 = vp
        sup.set_clip(pygame.Rect(x0, y0, x1 - x0 + 1, y1 - y0 + 1))


def fora_da_viewport(pts, vp):
    """True se a caixa envolvente do polígono (já em coordenadas de tela) não toca a viewport."""
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return max(xs) < vp[0] or min(xs) > vp[2] or max(ys) < vp[1] or min(ys) > vp[3]


class Renderizador:
    def __init__(self, sup, textura):
        self.sup = sup
        self.tex = textura
        self.tex_w, self.tex_h = textura.get_size()

    def para_tela(self, pts, m):
        """Mundo -> dispositivo: aplica a matriz janela->viewport."""
        return aplica_transformacao(m, pts)

    def linha(self, p0, p1, win, m, cor):
        """Recorta a reta contra a janela (Cohen-Sutherland), mapeia para a viewport e rasteriza."""
        vis, x0, y0, x1, y1 = cohen_sutherland(p0[0], p0[1], p1[0], p1[1], *win)
        if not vis:
            return
        (ax, ay), (bx, by) = aplica_transformacao(m, [(x0, y0), (x1, y1)])
        bresenham(self.sup, round(ax), round(ay), round(bx), round(by), cor)

    def desenhar_mundo(self, jogo, win, vp, detalhe=True):
        sup = self.sup
        clip_viewport(sup, vp)
        limpar(sup, BG_MAIN if detalhe else BG_MINI, vp)
        m = janela_viewport(win, vp)          # matriz janela -> viewport (uma vez por quadro)

        if detalhe:
            for gx in range(0, WORLD_W + 1, 60):
                self.linha((gx, 0), (gx, WORLD_H), win, m, GRID_COLOR)
            for gy in range(0, WORLD_H + 1, 60):
                self.linha((0, gy), (WORLD_W, gy), win, m, GRID_COLOR)
        for a, b in [((0, 0), (WORLD_W, 0)), ((WORLD_W, 0), (WORLD_W, WORLD_H)),
                     ((WORLD_W, WORLD_H), (0, WORLD_H)), ((0, WORLD_H), (0, 0))]:
            self.linha(a, b, win, m, WALL_COLOR)

        for b in jogo.bricks:
            pts = self.para_tela(b.polygon(), m)
            if fora_da_viewport(pts, vp):
                continue
            if detalhe:
                scanline_fill_gradiente(sup, pts, b.vertex_colors())
            else:
                scanline_fill(sup, pts, b.light)

        p = jogo.paddle
        pts = self.para_tela(p.polygon(), m)
        if fora_da_viewport(pts, vp):
            pass
        elif detalhe:
            scanline_texture(sup, pts, p.uvs, self.tex, self.tex_w, self.tex_h)
        else:
            scanline_fill(sup, pts, (200, 200, 230))

        pts = self.para_tela(jogo.ball.polygon(), m)
        if fora_da_viewport(pts, vp):
            return
        if detalhe:
            scanline_fill_gradiente(sup, pts, jogo.ball.vertex_colors())
        else:
            scanline_fill(sup, pts, WHITE)

    def desenhar_minimapa(self, jogo):
        full = (0, 0, WORLD_W, WORLD_H)
        self.desenhar_mundo(jogo, full, VP_MINI, detalhe=False)
        m = janela_viewport(full, VP_MINI)
        x0, y0, x1, y1 = jogo.window.tuple()
        for a, b in [((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)),
                     ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))]:
            self.linha(a, b, full, m, (255, 255, 0))

    def desenhar_jogo(self, jogo):
        sup = self.sup
        clip_viewport(sup, None)
        limpar(sup, (10, 10, 20))
        self.desenhar_mundo(jogo, jogo.window.tuple(), VP_MAIN)
        self.desenhar_minimapa(jogo)
        clip_viewport(sup, None)
        self._hud(jogo)
        self._overlay(jogo)

    def _hud(self, jogo):
        x = 492
        agendar_texto(x, 140, f"PONTOS {jogo.score}", WHITE)
        agendar_texto(x, 158, f"VIDAS {jogo.lives}", WHITE)
        agendar_texto(x, 176, f"ZOOM {jogo.window.zoom_level:.1f}X", WHITE)
        if jogo.follow:
            agendar_texto(x, 194, "SEGUE BOLA", (255, 220, 80))
        ajuda = ["SETAS MOVE", "ESPAÇO LANÇA", "Z X ZOOM", "IJKL JANELA",
                 "F SEGUE", "C RESET", "P PAUSA", "ESC MENU"]
        for i, t in enumerate(ajuda):
            agendar_texto(x, 222 + i * 14, t, (140, 140, 170))

    def _overlay(self, jogo):
        msg = {"over": "FIM DE JOGO", "won": "VOCÊ VENCEU", "paused": "PAUSA"}.get(jogo.state)
        if not msg:
            return
        sup = self.sup
        w = largura_texto(msg, 3)
        x = (WORLD_W - w) // 2
        scanline_fill(sup, retangulo_pts(x - 12, 170, x + w + 12, 230), (0, 0, 0))
        agendar_texto(x, 176, msg, (255, 220, 80), 3)
        if jogo.state in ("over", "won"):
            t = "R REINICIA"
            agendar_texto((WORLD_W - largura_texto(t, 2)) // 2, 208, t, WHITE, 2)
