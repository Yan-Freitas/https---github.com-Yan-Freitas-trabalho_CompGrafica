from lib.Motor_grafico import setPixel

def contorno_circulo(sup, xc, yc, r, cor):
    """Circunferência (ponto médio) só com o contorno, para usar com Boundary Fill."""
    x, y, d = 0, r, 1 - r
    while x <= y:
        for px, py in ((x, y), (y, x), (-x, y), (-y, x), (x, -y), (y, -x), (-x, -y), (-y, -x)):
            setPixel(sup, xc + px, yc + py, cor)
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1

def _quatro(sup, xc, yc, x, y, cor):
    for sx in (-1, 1):
        for sy in (-1, 1):
            setPixel(sup, xc + sx * x, yc + sy * y, cor)

def contorno_elipse(sup, xc, yc, rx, ry, cor):
    """Elipse (ponto médio) só com o contorno."""
    x, y = 0, ry
    rx2, ry2 = rx * rx, ry * ry
    dx, dy = 0, 2 * rx2 * y
    p1 = ry2 - rx2 * ry + 0.25 * rx2
    while dx < dy:
        _quatro(sup, xc, yc, x, y, cor)
        x += 1
        dx += 2 * ry2
        if p1 < 0:
            p1 += dx + ry2
        else:
            y -= 1
            dy -= 2 * rx2
            p1 += dx - dy + ry2
    p2 = ry2 * (x + 0.5) ** 2 + rx2 * (y - 1) ** 2 - rx2 * ry2
    while y >= 0:
        _quatro(sup, xc, yc, x, y, cor)
        y -= 1
        dy -= 2 * rx2
        if p2 > 0:
            p2 += rx2 - dy
        else:
            x += 1
            dx += 2 * ry2
            p2 += dx - dy + rx2
