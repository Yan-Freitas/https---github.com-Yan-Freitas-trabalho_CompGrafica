import math

def identidade():
    return [
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
    ]

def translacao(tx, ty):
    return [
    [1, 0, tx],
    [0, 1, ty],
    [0, 0, 1]
    ]

def escala(sx, sy):
    return [
    [sx, 0, 0],
    [0, sy, 0],
    [0, 0, 1]
    ]   

def rotacao(theta):
    theta_rad = math.radians(theta)
    c = math.cos(theta_rad)
    s = math.sin(theta_rad)
    return [
    [c, -s, 0],
    [s, c, 0],
    [0, 0, 1]    
    ]

def multiplica_matrizes(a, b):
    r = [[0]*3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                r[i][j] += a[i][k] * b[k][j]
    return r

def cria_transformacao():
    return identidade()

def aplica_transformacao(m, pontos):
    novos = []
    for x, y in pontos:
        v = [x, y, 1]
        x_novo = m[0][0]*v[0] + m[0][1]*v[1] + m[0][2]
        y_novo = m[1][0]*v[0] + m[1][1]*v[1] + m[1][2]
        novos.append((x_novo, y_novo))
    return novos