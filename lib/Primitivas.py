from lib.Motor_grafico import *
from lib.Recorte import *
from lib.Preenchimento import *

def bresenham(superficie, x0, y0, x1, y1, cor):
    steep = abs(y1 - y0) > abs(x1 - x0)
    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = y1 - y0

    ystep = 1
    if dy < 0:
        ystep = -1
        dy = -dy

    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)

    x = x0
    y = y0

    while x <= x1:
        if steep:
            setPixel(superficie, y, x, cor)
        else:
            setPixel(superficie, x, y, cor)

        if d <= 0:
            d += incE
        else:
            d += incNE
            y += ystep

        x += 1

def desenhar_poligono(superficie, pontos, cor_borda):
    n = len(pontos)
    for i in range(n):
        x0, y0 = pontos[i]
        x1, y1 = pontos[(i + 1) % n]
        bresenham(superficie, x0, y0, x1, y1, cor_borda)

def desenhar_poligono_recortado(superficie, pontos, janela, cor):
    xmin, ymin, xmax, ymax = janela
    n = len(pontos)

    for i in range(n):
        x0, y0 = pontos[i]
        x1, y1 = pontos[(i + 1) % n]

        visivel, rx0, ry0, rx1, ry1 = cohen_sutherland(
            x0, y0, x1, y1, xmin, ymin, xmax, ymax
        )

        if visivel:
            bresenham(superficie,
                    int(rx0), int(ry0),
                    int(rx1), int(ry1),
                    cor)

def desenhar_circulo(superficie, xc, yc, raio, cor):
    x = 0
    y = raio
    d = 1 - raio 

    one_scanline(superficie, xc - y, xc + y, yc, cor)
    while x < y:
        previous_y = y
        if d < 0:
            d = d + 2 * x + 3
        else:
            d = d + 2 * (x - y) + 5
            y -= 1
        x += 1
        
        one_scanline(superficie, xc - y, xc + y, yc+x, cor)
        one_scanline(superficie, xc - y, xc + y, yc-x, cor)
        
        if y < previous_y and previous_y != x:
            one_scanline(superficie, xc - (x - 1), xc + (x - 1), yc + previous_y, cor)
            one_scanline(superficie, xc - (x - 1), xc + (x - 1), yc - previous_y, cor)

def desenhar_elipse(superficie, xc, yc, rx, ry, cor):
    x = 0
    y = ry

    rx2 = rx * rx
    ry2 = ry * ry
    dois_rx2 = 2 * rx2
    dois_ry2 = 2 * ry2
    
    p1 = ry2 - (rx2 * ry) + (0.25 * rx2)
    dx = dois_ry2 * x
    dy = dois_rx2 * y
    
    while dx < dy:
        if p1 < 0:
            x += 1
            dx += dois_ry2
            p1 += dx + ry2
        else:
            one_scanline(superficie, xc - x, xc + x, yc + y, cor)
            if y != 0:
                one_scanline(superficie, xc - x, xc + x, yc - y, cor)
            
            x += 1
            y -= 1
            dx += dois_ry2
            dy -= dois_rx2
            p1 += dx - dy + ry2
            
    p2 = (ry2 * (x + 0.5) * (x + 0.5)) + (rx2 * (y - 1) * (y - 1)) - (rx2 * ry2)
    
    while y >= 0:
        one_scanline(superficie, xc - x, xc + x, yc + y, cor)
        if y != 0:
            one_scanline(superficie, xc - x, xc + x, yc - y, cor)
        
        if p2 > 0:
            y -= 1
            dy -= dois_rx2
            p2 += rx2 - dy
        else:
            y -= 1
            x += 1
            dx += dois_ry2
            dy -= dois_rx2
            p2 += dx - dy + rx2