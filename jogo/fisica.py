import math

def circle_rect(cx, cy, r, rx, ry, rw, rh):
    px = min(max(cx, rx), rx + rw)
    py = min(max(cy, ry), ry + rh)
    dx, dy = cx - px, cy - py
    d2 = dx * dx + dy * dy
    if d2 > r * r:
        return None
    if d2 == 0:
        return min([(cx - rx, (-1, 0)), (rx + rw - cx, (1, 0)),
                    (cy - ry, (0, -1)), (ry + rh - cy, (0, 1))])[1]
    d = math.sqrt(d2)
    return dx / d, dy / d

def limitar_angulo(vx, vy, min_vy=0.25):
    """Evita bola quase horizontal: garante |vy| >= min_vy * velocidade, mantendo a velocidade."""
    sp = math.hypot(vx, vy)
    if sp == 0 or abs(vy) >= min_vy * sp:
        return vx, vy
    vy = (-1 if vy <= 0 else 1) * min_vy * sp
    vx = math.copysign(math.sqrt(sp * sp - vy * vy), vx if vx != 0 else 1)
    return vx, vy


def reflect(vx, vy, nx, ny):
    dot = vx * nx + vy * ny
    if dot >= 0:
        return vx, vy
    return vx - 2 * dot * nx, vy - 2 * dot * ny
