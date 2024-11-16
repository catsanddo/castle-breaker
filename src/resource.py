import pygame as pg
from os import path

class Animation:
    def __init__(self, images, fps):
        self.frames = images
        self.frame = 0

        self.period = 1 / fps
        self.time = 0

    def get_image(self):
        return self.frames[self.frame]

    def update(self, tick):
        self.time += tick
        while self.time > self.period:
            self.time -= self.period
            self.frame += 1
            if self.frame >= len(self.frames):
                self.frame = 0

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
        "orb": pg.Rect(0, 0, 128, 128),
        "orb_chipped": pg.Rect(128, 0, 128, 128),
        "orb_cracked": pg.Rect(256, 0, 128, 128),
        "orb_shattered": pg.Rect(384, 0, 128, 128)
    }

    @classmethod
    def load_texture(cls, name):
        if cls.atlas == None:
            cls.atlas = pg.image.load(path.join("res", "atlas.png")).convert_alpha()

        # cache
        if name in cls.images:
            return cls.images[name]

        rect = cls.atlas_map[name]
        if type(rect) is list:
            frames = []
            for r in rect:
                surface = pg.Surface(r.size, pg.SRCALPHA, cls.atlas)
                surface.blit(cls.atlas, (0, 0), r)
                frames.append(surface)
            rect = rect[0]
            cls.images[name] = Animation(frames, 5)
        else:
            surface = pg.Surface(rect.size, pg.SRCALPHA, cls.atlas)
            surface.blit(cls.atlas, (0, 0), rect)
            cls.images[name] = surface
        return cls.images[name]
