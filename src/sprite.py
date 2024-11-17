import pygame as pg
import math
from resource import Manager
from game import Game, collide_ball, collide_balls

def reflect_vector(d, n):
    dn = d[0] * n[0] + d[1] * n[1]
    subx = 2 * dn * n[0]
    suby = 2 * dn * n[1]
    return (d[0] - subx, d[1] - suby)

def norm_vector(v):
    angle = 0
    if v[0] == 0:
        if v[1] < 0:
            anlge = math.pi / 2
        else:
            angle = math.pi * 3 / 2
    else:
        angle = math.atan(-v[1] / v[0])
        if (v[0] < 0):
            angle += math.pi
    wx = math.cos(angle)
    wy = math.sin(angle)
    return (wx, wy)

class Paddle(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = Manager.load_texture("paddle")
        self.rect = self.image.get_rect()
        self.rect.centerx = Game.WIDTH // 2
        self.rect.bottom = Game.HEIGHT - 64
        self.rect.height = 4
        self.bottom = Manager.load_texture("cart")

    def draw(self, surface):
        surface.blit(self.bottom.get_image(), (self.rect.x, Game.HEIGHT - 64))
        surface.blit(self.image, self.rect.topleft)
        if Game.DEBUG:
            pg.draw.rect(surface, (255, 255, 255), self.rect, 1)

    def update(self, dt):
        self.bottom.update(dt)

class Brick(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)

        self.image = Manager.load_texture("brick")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.health = 2
        self.hit = False

    def update(self):
        if self.hit:
            self.health -= 1
            if self.health == 1:
                self.image = Manager.load_texture("brick_broken")
            elif self.health == 0:
                self.kill()
            self.hit = False

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

    def update(self, paddle, orb, collisions):
        if self.is_out_of_side():
            self.vel_x *= -1
        if self.is_out_of_top():
            self.vel_y *= -1
        elif self.is_out_of_bottom():
            self.kill()

        collisions = collisions.get(self)

        was_hit = False
        if collisions:
            for collider in collisions:
                if not was_hit:
                    if self.rect.top < collider.rect.bottom and \
                        self.rect.bottom > collider.rect.bottom:
                        self.vel_y *= -1
                        self.rect.top = collider.rect.bottom + 1
                    elif self.rect.bottom > collider.rect.top and \
                        self.rect.top < collider.rect.top:
                        self.vel_y *= -1
                        self.rect.bottom = collider.rect.top - 1
                    if self.rect.right > collider.rect.left and \
                        self.rect.left < collider.rect.left:
                        self.vel_x *= -1
                        self.rect.right = collider.rect.left - 1
                    elif self.rect.left < collider.rect.right and \
                        self.rect.right > collider.rect.right:
                        self.vel_x *= -1
                        self.rect.left = collider.rect.right + 1
                collider.hit = True
                was_hit = True
                
        # Special paddle collision
        if collide_ball(self, paddle):
            self.vel_y *= -1

            angle = self.get_vel_angle()
            x = self.rect.centerx - paddle.rect.centerx
            angle += -x / (paddle.rect.width // 2) * (math.pi / 4)
            angle = pg.math.clamp(angle, math.pi / 6, math.pi * 5 / 6)

            self.set_vel_angle(angle)
            # Move ball out of paddle to prevent double bounce
            self.rect.centery = paddle.rect.y - 8

        # Special orb collision
        if collide_balls(self, orb):
            dist = (self.rect.centerx - orb.rect.centerx, self.rect.centery - orb.rect.centery)
            n = norm_vector(dist)
            self.rect.centerx = orb.rect.centerx + n[0] * (self.radius + orb.radius)
            self.rect.centery = orb.rect.centery + -n[1] * (self.radius + orb.radius)

            self.vel_x, self.vel_y = reflect_vector((self.vel_x, self.vel_y), n)
            self.vel_x *= -1
            self.vel_y *= -1

            orb.hit = True

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

class Orb:
    def __init__(self):
        self.image = Manager.load_texture("orb")
        self.rect = self.image.get_rect()

        self.rect.centerx = Game.WIDTH // 2
        self.rect.top = 32

        self.radius = 60

        self.health = 3
        self.hit = False
        self.cooldown = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        if Game.DEBUG:
            pg.draw.circle(surface, (255, 255, 255), self.rect.center, self.radius, 1)

    def update(self):
        if self.hit and self.cooldown <= 0:
            self.health -= 1
            self.cooldown = 30
            textures = ("orb_shattered", "orb_cracked", "orb_chipped")
            self.image = Manager.load_texture(textures[self.health])
        self.hit = False
        self.cooldown -= 1
        if self.cooldown < 0:
            self.cooldown = 0
