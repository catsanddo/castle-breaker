import pygame as pg
from os import path

class Manager:
    COLOR_KEY = (255, 16, 255)

    images = {}
    atlas = None
    atlas_map = {
        "ball": pg.Rect(384, 192, 16, 16),
        "paddle": pg.Rect(256, 128, 128, 16),
        "cart": [
            pg.Rect(256, 144, 128, 16),
            pg.Rect(256, 160, 128, 16),
            pg.Rect(256, 176, 128, 16)
        ],
        "brick": pg.Rect(256, 192, 128, 32),
        "brick_broken": pg.Rect(256, 224, 128, 32),
        "grass": pg.Rect(384, 128, 64, 64),
        "cobble": pg.Rect(448, 128, 64, 64),
        "dragon_sleeping": [
            pg.Rect(0, 0, 256, 128),
            pg.Rect(256, 0, 256, 128),
        ],
        "dragon_nervous": pg.Rect(0, 128, 256, 128)
    }

    @classmethod
    def load_texture(cls, name):
        if cls.atlas == None:
            cls.atlas = pg.image.load(path.join("res", "atlas.png")).convert_alpha()

        # cache
        if name in cls.images:
            return cls.images[name]

        print(name)

        rect = cls.atlas_map[name]
        surface = pg.Surface(rect.size, pg.SRCALPHA, cls.atlas)
        surface.blit(cls.atlas, (0, 0), rect)
        cls.images[name] = surface
        return cls.images[name]
