import logging
import pygame as pg

class Map:
    def __init__(self):
        self.background: pg.Surface = None

        self.position = (0, 0)

    def load(self):
        logging.info("Loading map")
        self.background = pg.image.load("assets/images/backgrounds/map.png")

    def draw(self, screen):
        screen.blit(self.background, self.position)
        screen.blit(
            self.background,
            (
                self.position[0] + self.background.get_width(),
                self.position[1],
            )
        )

    def update(self, truckSpeed: float, timeElapsed: float):
        self.position = (
            self.position[0] - truckSpeed * timeElapsed,
            self.position[1],
        )

        if self.position[0] < -self.background.get_width():
            self.position = (0, 0)