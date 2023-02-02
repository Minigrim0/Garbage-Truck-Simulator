import pygame as pg
import logging

from GTS.interface.menus.menu import Menu
from GTS.abstracts.runnable import Runnable
from GTS.models.game import Game


class GameIntro(Menu, Runnable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.advice: pg.Surface = None

        self._build()

    def _build(self):
        self.advice = pg.image.load("assets/images/backgrounds/conseils.png")

    def loop(self):
        super().loop()

        self.handleEvents()

        self.draw()
        self.screen.flip()

    def draw(self):
        self.screen.blit(self.advice, (0, 0))

    def handleEvents(self):
        for event in super().handleEvent():
            if event.type == pg.KEYDOWN:
                self.launch("game")

    def launch(self, toLaunch: str):
        if toLaunch == "game":
            logging.info("Launching game")
            Game.getInstance(self.screen)()
            self.running = False
