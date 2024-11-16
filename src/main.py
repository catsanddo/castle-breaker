import pygame as pg
import math
import sprite
from game import Game

def main():
    # Init the display
    pg.display.set_mode((Game.WIDTH, Game.HEIGHT))

    playing = True
    while playing:
        game = Game()
        # Game.run() returns True to play again
        playing = game.run()

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
