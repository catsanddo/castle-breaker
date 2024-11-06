import pygame as pg
import math
import sprite
from game import Game

class Paddle:
    def __init__(self):
        self.width = 100
        self.height = 15
        self.x = Game.WIDTH // 2 - self.width // 2
        self.y = Game.HEIGHT - 50

        self.color = pg.Color(25, 25, 25)

    def get_rect(self):
        return pg.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        return pg.draw.rect(surface, self.color, self.get_rect())

    def collide_ball(self, ball):
        if self.y - ball.rect.centery < ball.radius and ball.rect.centery - (self.y + self.height) < ball.radius and self.x - ball.rect.centerx < ball.radius and ball.rect.centerx - (self.x + self.width) < ball.radius:
            return True
        return False

def main():
    screen = pg.display.set_mode((Game.WIDTH, Game.HEIGHT))
    screen.fill(pg.Color(150, 0, 0))
    pg.display.flip()
    
    clock = pg.time.Clock()

    paddle = Paddle()
    balls = pg.sprite.Group()

    running = True
    while running:
        mouse_pos = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                ball_x = paddle.x + paddle.width // 2
                ball_y = paddle.y - 8
                balls.add(sprite.Ball(ball_x, ball_y))

        # Update
        paddle.x = mouse_pos[0] - paddle.width // 2

        balls.update(paddle)

        # Draw
        screen.fill(pg.Color(150, 0, 0))

        paddle.draw(screen)

        balls.draw(screen)

        pg.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
