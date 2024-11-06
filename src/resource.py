from pygame import image
from os import path

class Manager:
    images = {}

    @classmethod
    def load_texture(cls, name):
        if name in cls.images:
            return cls.images[name]
        surface = image.load(path.join("res", "images", f"{name}.png"))
        cls.images[name] = surface.convert_alpha()
        return cls.images[name]
