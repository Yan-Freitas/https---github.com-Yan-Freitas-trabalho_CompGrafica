import math
import pygame
from jogo.config import *
from jogo.entidades import Paddle, Ball, Brick
from jogo.fisica import circle_rect, reflect, limitar_angulo
from jogo.janela import Janela


class Partida:
    def __init__(self, speed_mult=1.0):
        self.speed_mult = speed_mult
        self.window = Janela()
        self.follow = False
        self.reset()

    def reset(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = [Brick(r, c) for r in range(BRICK_ROWS) for c in range(BRICK_COLS)]
        self.score, self.lives = 0, 3
        self.state = "ready"          # ready | playing | paused | over | won
        self.window.reset()
        self._stick_ball()

    def _stick_ball(self):
        b, p = self.ball, self.paddle
        b.x, b.y = p.x, p.top - b.r - 1
        b.vx = b.vy = 0.0

    def keydown(self, key):
        if key == pygame.K_SPACE and self.state == "ready":
            sp = BALL_SPEED * self.speed_mult
            a = math.radians(25)
            self.ball.vx, self.ball.vy = sp * math.sin(a), -sp * math.cos(a)
            self.state = "playing"
        elif key == pygame.K_p:
            if self.state == "playing":
                self.state = "paused"
            elif self.state == "paused":
                self.state = "playing"
        elif key == pygame.K_f:
            self.follow = not self.follow
        elif key == pygame.K_c:
            self.window.reset()
        elif key == pygame.K_r and self.state in ("over", "won"):
            self.reset()

    def update(self, dt, keys):
        self._update_window(dt, keys)
        if self.state in ("paused", "over", "won"):
            return

        for br in self.bricks:
            br.update(dt)
        self.bricks = [br for br in self.bricks if not br.gone]

        self.paddle.move((keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * PADDLE_SPEED * dt)

        if self.state == "ready":
            self._stick_ball()
            return
        passos = max(3, math.ceil(dt * 90))      # mais subpassos se o quadro demorar
        for _ in range(passos):
            self._step(dt / passos)

        if not any(br.alive for br in self.bricks):
            self.state = "won"

    def _update_window(self, dt, keys):
        w = self.window
        if keys[pygame.K_z]:
            w.zoom(1 + 1.5 * dt)
        if keys[pygame.K_x]:
            w.zoom(1 / (1 + 1.5 * dt))
        k = PAN_SPEED * dt * (w.width / WORLD_W)
        dx = (keys[pygame.K_l] - keys[pygame.K_j]) * k
        dy = (keys[pygame.K_k] - keys[pygame.K_i]) * k
        if dx or dy:
            w.pan(dx, dy)
        if self.follow:
            w.center_on(self.ball.x, self.ball.y, min(1.0, 6 * dt))

    def _step(self, dt):
        b, p = self.ball, self.paddle
        b.x += b.vx * dt
        b.y += b.vy * dt

        if b.x - b.r < 0:
            b.x, b.vx = b.r, abs(b.vx)
        elif b.x + b.r > WORLD_W:
            b.x, b.vx = WORLD_W - b.r, -abs(b.vx)
        if b.y - b.r < 0:
            b.y, b.vy = b.r, abs(b.vy)

        if b.vy > 0 and circle_rect(b.x, b.y, b.r, p.left, p.top, p.width, p.h):
            off = max(-1.0, min(1.0, (b.x - p.x) / (p.width / 2)))
            ang = off * math.radians(60)
            sp = math.hypot(b.vx, b.vy)
            b.vx, b.vy = sp * math.sin(ang), -sp * math.cos(ang)
            b.y = p.top - b.r - 0.01

        for br in self.bricks:
            if br.alive:
                n = circle_rect(b.x, b.y, b.r, br.x, br.y, BRICK_W, BRICK_H)
                if n:
                    b.vx, b.vy = reflect(b.vx, b.vy, *n)
                    b.vx, b.vy = limitar_angulo(b.vx, b.vy)
                    br.hit()
                    self.score += 10 * (BRICK_ROWS - br.row)
                    break

        if b.y - b.r > WORLD_H:
            self.lives -= 1
            if self.lives <= 0:
                self.state = "over"
            else:
                self.state = "ready"
                self._stick_ball()
