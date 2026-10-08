import pygame

_fontes = {}
_cache = {}
_fila = []          # textos pedidos durante o quadro: (x, y, texto, cor, escala)


def _fonte(escala):
    tam = 8 * escala                      # escala 2 -> 16 px, 3 -> 24 px, 8 -> 64 px
    if tam not in _fontes:
        if not pygame.font.get_init():
            pygame.font.init()
        _fontes[tam] = pygame.font.Font(None, tam)
    return _fontes[tam]


def largura_texto(texto, escala=2):
    return _fonte(escala).size(texto)[0]


def agendar_texto(x, y, texto, cor, escala=2):
    """Pede um texto para este quadro; ele é escrito sobre a tela por desenhar_fila()."""
    _fila.append((x, y, texto, cor, escala))


def desenhar_fila(tela):
    """Chamar depois de tela.blit(framebuffer): render + blit de cada texto pedido."""
    for x, y, texto, cor, escala in _fila:
        chave = (texto, tuple(cor), escala)
        if chave not in _cache:
            if len(_cache) > 500:
                _cache.clear()
            _cache[chave] = _fonte(escala).render(texto, 1, cor)
        tela.blit(_cache[chave], (x, y))
    _fila.clear()
