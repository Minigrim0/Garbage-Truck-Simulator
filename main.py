import logging

import pygame as pg

from GTS.models.gts import GarbageTruckSimulator

logging.basicConfig(level=logging.DEBUG)

logging.info("Initializing pygame")
pg.init()
pg.key.set_repeat(10, 10)

logging.info("launching game")
gts = GarbageTruckSimulator.getInstance()
gts()
