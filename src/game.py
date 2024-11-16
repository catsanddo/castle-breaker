import pygame as pg
import math
from random import random
import sprite
from resource import Manager

def collide_ball(ball, sprite):
    if sprite.rect.y - ball.rect.centery < ball.radius and \
        ball.rect.centery - (sprite.rect.bottom) < ball.radius and \
        sprite.rect.x - ball.rect.centerx < ball.radius and \
        ball.rect.centerx - (sprite.rect.right) < ball.radius:
        return True
    return False

def collide_balls(b1, b2):
    if (b1.rect.centerx - b2.rect.centerx) ** 2 + \
        (b1.rect.centery - b2.rect.centery) ** 2 < \
        b1.radius ** 2 + b2.radius ** 2:
        return True
    return False

def randrange(min, max):
    range = max - min
    return range * random() + min

def debug_text(text, x, y):
    font = pg.font.SysFont(pg.font.get_default_font(), 20)
    surface = font.render(text, True, (255, 255 ,255))
    screen = pg.display.get_surface()
    screen.blit(surface, (x, y))

def game_text(text, x, y, centered=True):
    font = pg.font.SysFont(pg.font.get_default_font(), 75)
    surface = font.render(text, True, (255, 255, 255))
    if centered:
        x -= surface.get_rect().w // 2
    screen = pg.display.get_surface()
    screen.blit(surface, (x, y))

class Game:
    WIDTH = 640
    HEIGHT = 768
    DEBUG = False

    def __init__(self):
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pg.time.Clock()
        self.won = False
        self.lost = False

        self.paddle = sprite.Paddle()
        self.orb = sprite.Orb()
        self.balls = pg.sprite.Group()
        self.bricks = pg.sprite.Group()

        # The player gets this many balls to launch
        self.ball_count = 1

        # Drawing the background layer from tiles
        self.background = pg.Surface((self.WIDTH, self.HEIGHT), 0, Manager.atlas)
        for y in range(0, self.HEIGHT // 2, 64):
            for x in range(0, self.WIDTH, 64):
                self.background.blit(Manager.load_texture("cobble"), (x, y))
        for y in range(self.HEIGHT // 2, self.HEIGHT, 64):
            for x in range(0, self.WIDTH + 64, 64):
                x_offset = -32 * (y // 64 % 2)
                self.background.blit(Manager.load_texture("grass"), (x + x_offset, y))

        # Create bricks
        for y in range(4):
            for x in range(6):
                x_offset = 64 * int(not(y % 2 != 0)) - 128
                brick = sprite.Brick(x * 128 + x_offset, y * 32 + 256)
                self.bricks.add(brick)
        for x in range(3):
            brick = sprite.Brick(x * 256, 224)
            self.bricks.add(brick)

        self.screen.fill((255, 255, 255))
        self.screen.blit(self.background, (0, 0))
        pg.display.flip()

    def run(self):
        running = True
        while running:
            mouse_pos = pg.mouse.get_pos()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    ball_x = self.paddle.rect.centerx
                    ball_y = self.paddle.rect.y - 8
                    if Game.DEBUG or self.ball_count > 0:
                        start = True
                        ball = sprite.Ball(ball_x, ball_y)
                        angle = randrange(math.pi / 4, math.pi * 3 / 4)
                        if not Game.DEBUG:
                            self.ball_count -= 1
                            ball.set_vel_angle(angle)
                        self.balls.add(ball)
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_z:
                        Game.DEBUG = not Game.DEBUG
                    
            # Update
            if not self.won and not self.lost:
                self.paddle.rect.centerx = mouse_pos[0]
                self.paddle.rect.x = pg.math.clamp(self.paddle.rect.x, 0, self.WIDTH - self.paddle.rect.w)

                self.paddle.update(self.clock.get_time() / 1000)

                collisions = pg.sprite.groupcollide(self.balls, self.bricks, False, False, collide_ball)
                self.balls.update(self.paddle, self.orb, collisions)
                self.bricks.update()
                self.orb.update()

            if self.orb.health == 0:
                self.won = True
            elif self.ball_count <= 0 and len(self.balls) <= 0:
                self.lost = True

            # Draw
            # self.screen.fill(pg.Color(150, 150, 150))
            self.screen.blit(self.background, (0, 0))

            self.paddle.draw(self.screen)
            self.orb.draw(self.screen)
            self.bricks.draw(self.screen)

            self.balls.draw(self.screen)

            if self.won:
                game_text("You Won!", Game.WIDTH // 2, 180)
            elif self.lost:
                game_text("You Lost", Game.WIDTH // 2, 180)
            elif len(self.balls) <= 0:
                game_text("Click to start!", Game.WIDTH // 2, 180)

            if self.DEBUG:
                for y in range(12):
                    h = 64
                    color = (0, 255, 0)
                    if y % 3 == 0:
                        color = (0, 0, 255)
                    pg.draw.line(self.screen, color, (0, y*h), (self.WIDTH, y*h))
                # Orb sprite box
                rect = pg.Rect(0, 0, 128, 128)
                rect.centerx = self.WIDTH // 2
                rect.y = 32

                debug_text(f"Balls: {len(self.balls)}", 10, 10)
                pg.draw.rect(self.screen, (255, 255, 255), rect, 1)

            pg.display.flip()
            self.clock.tick(60)
