import logging

import pygame

from models.gts import GarbageTruckSimulator

logging.basicConfig(level=logging.WARNING)

logging.info("Initializing pygame")
pygame.init()

logging.info("launching game")
gts = GarbageTruckSimulator.getInstance()
gts.run()
