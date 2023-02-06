import pygame as pg


class Sprite:
    def __init__(
        self,
        sprite: pg.Surface = None,
        flippable: bool = False,
        flipped: bool = False,
        position: tuple = (-1, -1),
        rotation: float = 0.0,
        drawing_offset: tuple = None):

        self.image = sprite
        self.flipped_image = None
        self.flippable = flippable
        self.flipped = flipped
        self.offset = drawing_offset

        if self.flippable and self.image is not None:
            self.flipped_image = pg.transform.flip(self.image, True, False)

    def flip(self):
        self.flipped = not self.flipped

    def update(self, elapsed_time: float):
        pass

    def draw(self, screen):
        screen.blit()
