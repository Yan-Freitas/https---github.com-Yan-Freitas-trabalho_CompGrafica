from lib.Motor_grafico import *

def boundary_fill(superficie, x, y, cor_preenchimento, cor_borda):
    largura = superficie.get_width()
    altura = superficie.get_height()

    pilha = [(x, y)]

    while pilha:
        x, y = pilha.pop()

        if not (0 <= x < largura and 0 <= y < altura):
            continue

        cor_atual = superficie.get_at((int(x), int(y)))[:3]

        if cor_atual == cor_borda or cor_atual == cor_preenchimento:
            continue

        setPixel(superficie, x, y, cor_preenchimento)

        pilha.append((x + 1, y))
        pilha.append((x - 1, y))
        pilha.append((x, y + 1))
        pilha.append((x, y - 1))

def scanline_fill(superficie, pontos, cor_preenchimento):
    ys = [p[1] for p in pontos]
    y_min = min(ys)
    y_max = max(ys)

    n = len(pontos)

    for y in range(int(y_min), int(y_max)):
        intersecoes_x = []

        for i in range(n):
            x0, y0 = pontos[i]
            x1, y1 = pontos[(i + 1) % n]

            if y0 == y1:
                continue

            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0

            if y < y0 or y >= y1:
                continue

            x = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
            intersecoes_x.append(x)

        intersecoes_x.sort()

        for i in range(0, len(intersecoes_x), 2):
            if i + 1 < len(intersecoes_x):
                x_inicio = int(round(intersecoes_x[i]))
                x_fim = int(round(intersecoes_x[i + 1]))

                for x in range(x_inicio, x_fim + 1):
                    setPixel(superficie, x, y, cor_preenchimento)

def interpola_cor(c1, c2, t):
    r = int(c1[0] + (c2[0]-c1[0])*t)
    g = int(c1[1] + (c2[1]-c1[1])*t)
    b = int(c1[2] + (c2[2]-c1[2])*t)

    r = max(0, min(r, 255))
    g = max(0, min(g, 255))
    b = max(0, min(b, 255))
    
    return (r, g, b)

def scanline_fill_gradiente(superficie, pontos, cores):
    ys = [p[1] for p in pontos]
    y_min = int(min(ys))
    y_max = int(max(ys))

    n = len(pontos)

    for y in range(y_min, y_max):
        intersecoes = []

        for i in range(n):
            x0, y0 = pontos[i]
            x1, y1 = pontos[(i + 1) % n]

            c0 = cores[i]
            c1 = cores[(i + 1) % n]

            if y0 == y1:
                continue

            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
                c0, c1 = c1, c0

            if y < y0 or y >= y1:
                continue

            t = (y - y0) / (y1 - y0)
            x = x0 + t * (x1 - x0)
            cor_y = interpola_cor(c0, c1, t)

            intersecoes.append((x, cor_y))

        intersecoes.sort(key=lambda i: i[0])

        for i in range(0, len(intersecoes), 2):
            if i + 1 < len(intersecoes):
                x_ini, cor_ini = intersecoes[i]
                x_fim, cor_fim = intersecoes[i + 1]

                if x_fim == x_ini:
                    continue

                for x in range(int(x_ini), int(x_fim) + 1):
                    t = (x - x_ini) / (x_fim - x_ini)
                    cor = interpola_cor(cor_ini, cor_fim, t)
                    setPixel(superficie, x, y, cor)

def scanline_texture(superficie, pontos, uvs, textura, tex_w, tex_h):
    n = len(pontos)

    ys = [p[1] for p in pontos]
    y_min = max(0, int(min(ys)))
    y_max = min(superficie.get_height(), int(max(ys)))

    for y in range(y_min, y_max):
        inter = []

        for i in range(n):
            x0, y0 = pontos[i]
            x1, y1 = pontos[(i + 1) % n]

            u0, v0 = uvs[i]
            u1, v1 = uvs[(i + 1) % n]

            if y0 == y1:
                continue

            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
                u0, v0, u1, v1 = u1, v1, u0, v0

            if y < y0 or y >= y1:
                continue

            t = (y - y0) / (y1 - y0)

            x = x0 + t * (x1 - x0)
            u = u0 + t * (u1 - u0)
            v = v0 + t * (v1 - v0)

            inter.append((x, u, v))

        inter.sort(key=lambda i: i[0])

        for i in range(0, len(inter), 2):
            if i + 1 >= len(inter):
                continue

            x_start, u_start, v_start = inter[i]
            x_end,   u_end,   v_end   = inter[i + 1]

            if x_start == x_end:
                continue
                
            x_start_math = int(x_start)
            x_end_math = int(x_end)
            
            dx = x_end_math - x_start_math
            
            passo_u = (u_end - u_start) / dx if dx != 0 else 0
            passo_v = (v_end - v_start) / dx if dx != 0 else 0

            x_start_clamp = max(0, x_start_math)
            x_end_clamp = min(superficie.get_width() - 1, x_end_math)

            offset_x = x_start_clamp - x_start_math
            u_atual = u_start + (passo_u * offset_x)
            v_atual = v_start + (passo_v * offset_x)

            for x in range(x_start_clamp, x_end_clamp + 1):
                tx = int(u_atual * (tex_w - 1))
                ty = int(v_atual * (tex_h - 1))

                if 0 <= tx < tex_w and 0 <= ty < tex_h:
                    cor = textura.get_at((tx, ty))
                    if cor.a > 0:
                        setPixel(superficie, x, y, cor)
                
                u_atual += passo_u
                v_atual += passo_v

def one_scanline(superficie, x_inicial, x_final, y, cor):
    for xp in range(int(x_inicial), int(x_final)+1):
        setPixel(superficie, xp, y, cor)

def scan_column(superficie, y_inicial, y_final, x, cor):
    for yp in range(int(y_inicial), int(y_final)+1):
        setPixel(superficie, x, yp, cor)