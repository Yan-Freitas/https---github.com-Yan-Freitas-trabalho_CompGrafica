from lib.Transformacoes import (translacao, escala, rotacao,
                                multiplica_matrizes, aplica_transformacao)

def _em_torno_de(m, cx, cy):
    """T(cx,cy) · M · T(-cx,-cy): aplica M tendo (cx,cy) como origem."""
    if cx == 0 and cy == 0:
        return m
    return multiplica_matrizes(translacao(cx, cy),
                               multiplica_matrizes(m, translacao(-cx, -cy)))

def transladar(pontos, dx, dy):
    return aplica_transformacao(translacao(dx, dy), pontos)

def escalar(pontos, sx, sy, cx=0, cy=0):
    return aplica_transformacao(_em_torno_de(escala(sx, sy), cx, cy), pontos)

def rotacionar(pontos, graus, cx=0, cy=0):
    """Ângulo em GRAUS (igual à sua rotacao)."""
    return aplica_transformacao(_em_torno_de(rotacao(graus), cx, cy), pontos)
