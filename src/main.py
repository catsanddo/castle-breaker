import pygame as pg
import math

WIDTH = 650
HEIGHT = 500

class Paddle:
    def __init__(self):
        self.width = 100
        self.height = 15
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 50

        self.color = pg.Color(25, 25, 25)

    def get_rect(self):
        return pg.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        return pg.draw.rect(surface, self.color, self.get_rect())

    def collide_ball(self, ball):
        if self.y - ball.y < ball.radius and ball.y - (self.y + self.height) < ball.radius and self.x - ball.x < ball.radius and ball.x - (self.x + self.width) < ball.radius:
            return True
        return False

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 8

        self.vel_x = 0
        self.vel_y = -1
        self.speed = 6

        self.color = pg.Color(200, 200, 200)

    def draw(self, surface):
        return pg.draw.circle(surface, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.vel_x * self.speed
        self.y += self.vel_y * self.speed

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
        if self.y < 0:
            return True
        return False

    def is_out_of_side(self):
        if self.x < 0 or self.x >= WIDTH:
            return True
        return False

    def is_out_of_bottom(self):
        if self.y >= HEIGHT:
            return True
        return False

def main():
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    screen.fill(pg.Color(150, 0, 0))
    pg.display.flip()
    
    clock = pg.time.Clock()

    paddle = Paddle()
    balls = []

    running = True
    while running:
        mouse_pos = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                ball_x = paddle.x + paddle.width // 2
                ball_y = paddle.y - 8
                balls.append(Ball(ball_x, ball_y))

        # Update
        paddle.x = mouse_pos[0] - paddle.width // 2

        dead_balls = []
        for i, ball in enumerate(balls):
            if ball.is_out_of_side():
                ball.vel_x *= -1
            if ball.is_out_of_top():
                ball.vel_y *= -1
            elif ball.is_out_of_bottom():
                dead_balls.append(i)

            if paddle.collide_ball(ball):
                ball.vel_y *= -1

                angle = ball.get_vel_angle()
                x = ball.x - (paddle.x + paddle.width // 2)
                angle += -x / (paddle.width // 2) * (math.pi / 4)
                angle = pg.math.clamp(angle, math.pi / 6, math.pi * 5 / 6)

                ball.set_vel_angle(angle)
                # Move ball out of paddle to prevent double bounce
                ball.y = paddle.y - 8

            ball.move()

        for i in dead_balls:
            balls.pop(i)

        # Draw
        screen.fill(pg.Color(150, 0, 0))

        paddle.draw(screen)

        for ball in balls:
            ball.draw(screen)

        pg.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
