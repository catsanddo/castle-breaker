import pygame as pg
import math
from resource import Manager
from game import Game

class Ball(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        
        self.radius = 8
        self.image = Manager.load_texture("ball")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.vel_x = 0
        self.vel_y = -1
        self.speed = 6

    def update(self, paddle):
        if self.is_out_of_side():
            self.vel_x *= -1
        if self.is_out_of_top():
            self.vel_y *= -1
        elif self.is_out_of_bottom():
            self.kill()

        if paddle.collide_ball(self):
            self.vel_y *= -1

            angle = self.get_vel_angle()
            x = self.rect.centerx - (paddle.x + paddle.width // 2)
            angle += -x / (paddle.width // 2) * (math.pi / 4)
            angle = pg.math.clamp(angle, math.pi / 6, math.pi * 5 / 6)

            self.set_vel_angle(angle)
            # Move ball out of paddle to prevent double bounce
            self.rect.centery = paddle.y - 8

        self.rect.centerx += self.vel_x * self.speed
        self.rect.centery += self.vel_y * self.speed

    def get_vel_angle(self):
        if self.vel_x == 0:
            if self.vel_y < 0:
                return math.pi / 2
            return math.pi * 3 / 2
        angle = math.atan(-self.vel_y / self.vel_x)
        if (self.vel_x < 0):
            angle += math.pi
        return angle

    def set_vel_angle(self, angle):
        mag = math.sqrt(self.vel_x * self.vel_x + self.vel_y * self.vel_y)
        self.vel_x = mag * math.cos(angle)
        self.vel_y = mag * math.sin(angle) * -1

    def is_out_of_top(self):
        if self.rect.top < 0:
            return True
        return False

    def is_out_of_side(self):
        if self.rect.left < 0 or self.rect.right >= Game.WIDTH:
            return True
        return False

    def is_out_of_bottom(self):
        if self.rect.bottom >= Game.HEIGHT:
            return True
        return False
