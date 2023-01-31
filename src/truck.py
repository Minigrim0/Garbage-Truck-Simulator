import math
import pygame

from utils import rot_center


class Truck(object):

    def __init__(self):
        self.Imgs = []
        self.Nitro = False
        self.PuissNitroBas
        self.PuissNitro

    def load(self):
        truckImg = pygame.image.load(
            "Images/CamionPoubelle.png").convert_alpha()

        for x in range(8):
            self.Imgs.append(
                rot_center(truckImg, 5 * math.sin(x * 180/math.pi)))
