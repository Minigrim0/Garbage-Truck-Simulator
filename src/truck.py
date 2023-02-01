import math
import logging
import pygame as pg

# from src.utils.rot_center import rot_center
from src.utils.bound import bound

class Truck(object):

    def __init__(self):
        self.image: pg.Surface = None
        self.Nitro = False

        self.position = (15, 800)
        self.health = 100
        self.speed = 30  # km/h
        self.steering_speed = 10

    @property
    def actual_speed(self):
        """
        Returns the truck speed in terms of pixels per second
        A meter is 64 pixels
        """
        return (self.speed / 3.6) * 64

    def load(self):
        logging.info("Loading truck")
        self.image = pg.image.load("assets/images/CamionPoubelle.png").convert_alpha()

    def draw(self, screen):
        screen.blit(self.image, self.position)

    def move(self, up: bool, timeElapsed: float):
        if up:
            self.position = (
                self.position[0],
                bound(350, 620, self.position[1] - self.steering_speed * timeElapsed),
            )
        else:
            self.position = (
                self.position[0],
                bound(350, 620, self.position[1] + self.steering_speed * timeElapsed),
            )

    def handleEvents(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_DOWN:
                self.move(False, 1)
            elif event.key == pg.K_UP:
                self.move(True, 1)
            elif event.key == pg.K_RIGHT:
                if not Constants.Nitro and not Constants.CamionPart:
                    Constants.Sounds["Nitro"].play()
                    Constants.Nitro = True
                    PuissNitroBas = Constants.PuissNitro
