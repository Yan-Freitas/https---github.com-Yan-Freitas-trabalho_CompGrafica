from lib.Transformacoes import *

def janela_viewport(janela, viewport):
    Wxmin, Wymin, Wxmax, Wymax = janela
    Vxmin, Vymin, Vxmax, Vymax = viewport

    sx = (Vxmax - Vxmin) / (Wxmax - Wxmin)
    sy = (Vymax - Vymin) / (Wymax - Wymin)

    m = identidade()

    m = multiplica_matrizes(translacao(-Wxmin, -Wymin), m)

    m = multiplica_matrizes(escala(sx, sy), m)

    m = multiplica_matrizes(translacao(Vxmin, Vymin), m)

    return m
