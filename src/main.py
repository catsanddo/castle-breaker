import pygame as pg
import math
import sprite
from game import Game

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
