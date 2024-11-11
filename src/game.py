import pygame as pg
import sprite
from resource import Manager

def collide_ball(ball, sprite):
    # if not isinstance(ball, sprite.Ball):
    #     return False
    if sprite.rect.y - ball.rect.centery < ball.radius and \
        ball.rect.centery - (sprite.rect.bottom) < ball.radius and \
        sprite.rect.x - ball.rect.centerx < ball.radius and \
        ball.rect.centerx - (sprite.rect.right) < ball.radius:
        return True
    return False

class Game:
    WIDTH = 640
    HEIGHT = 768
    DEBUG = False

    def __init__(self):
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pg.time.Clock()

        self.paddle = sprite.Paddle()
        self.balls = pg.sprite.Group()
        self.bricks = pg.sprite.Group()

        # Drawing the background layer from tiles
        self.background = pg.Surface((self.WIDTH, self.HEIGHT), 0, Manager.atlas)
        for y in range(0, self.HEIGHT // 2, 64):
            for x in range(0, self.WIDTH, 64):
                self.background.blit(Manager.load_texture("cobble"), (x, y))
        for y in range(self.HEIGHT // 2, self.HEIGHT, 64):
            for x in range(0, self.WIDTH, 64):
                self.background.blit(Manager.load_texture("grass"), (x, y))

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
                    self.balls.add(sprite.Ball(ball_x, ball_y))
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_z:
                        Game.DEBUG = not Game.DEBUG
                    
            # Update
            self.paddle.rect.centerx = mouse_pos[0]
            self.paddle.rect.x = pg.math.clamp(self.paddle.rect.x, 0, self.WIDTH - self.paddle.rect.w)

            collisions = pg.sprite.groupcollide(self.balls, self.bricks, False, False, collide_ball)
            self.balls.update(self.paddle, collisions)
            self.bricks.update()

            # Draw
            # self.screen.fill(pg.Color(150, 150, 150))
            self.screen.blit(self.background, (0, 0))

            self.paddle.draw(self.screen)

            self.balls.draw(self.screen)

            self.bricks.draw(self.screen)

            if self.DEBUG:
                for y in range(12):
                    h = 64
                    color = (0, 255, 0)
                    if y % 3 == 0:
                        color = (0, 0, 255)
                    pg.draw.line(self.screen, color, (0, y*h), (self.WIDTH, y*h))
                # Dragon sprite box
                rect = pg.Rect(0, 0, 256, 128)
                rect.centerx = self.WIDTH // 2
                rect.y = 32
                pg.draw.rect(self.screen, (255, 255, 255), rect, 1)

            pg.display.flip()
            self.clock.tick(60)
