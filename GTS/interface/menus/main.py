import os
import time
import random
import pygame as pg
import glob
from datetime import datetime

from GTS.models.gts import GarbageTruckSimulator
from GTS.abstracts.runnable import Runnable
from GTS.interface.menus.menu import Menu
from GTS.interface.menus.game_intro import GameIntro
from GTS.interface.components.button import Button

import logging
logger = logging.getLogger("[Menu][Main]")


class MainMenu(Menu, Runnable):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.percussion = (0, None)
        self.total_time = 0
        self.gameInstance = GarbageTruckSimulator.getInstance()

        self.background: pg.Surface = pg.Surface((1920, 1080))
        self.images = []

        self._build()

    def _build_buttons(self):
        self.buttons = {
            "play": Button((860, 500), (200, 50), callback=self.launch, toLaunch="game"),
            "options": Button((860, 600), (200, 50), callback=self.launch, toLaunch="options"),
            "credits": Button((860, 700), (200, 50), callback=self.launch, toLaunch="credits"),
            "quit": Button((860, 800), (200, 50), callback=self.launch, toLaunch="quit")
        }

        buttons_font = self.gameInstance.options.fonts["MedievalSharp-xOZ5"]["40"]
        self.buttons["play"].build("Play", buttons_font, ("CENTER", "CENTER"))
        self.buttons["options"].build("Options", buttons_font, ("CENTER", "CENTER"))
        self.buttons["credits"].build("Credits", buttons_font, ("CENTER", "CENTER"))
        self.buttons["quit"].build("Quit", buttons_font, ("CENTER", "CENTER"))

    def _build(self):
        self.gameInstance.options.play_music("frantic-15190")

        self.background.fill((190, 0, 0))
        self._build_buttons()

        options = self.gameInstance.options

        title = options.fonts["MedievalSharp-xOZ5"]["100"].render(
            "Garbage Truck Simulator®", 1, (0, 0, 0)
        )
        self.images.append(
            ((1920 / 2 - title.get_size()[0] / 2, 100 - title.get_size()[1] / 2), title)
        )

        copyright = options.fonts["MedievalSharp-xOZ5"]["20"].render(
            f"Minigrim0 © 2016 - {datetime.now().year}", 1, (0, 0, 0)
        )
        self.images.append(
            ((1920 - copyright.get_size()[0], 1080 - copyright.get_size()[1]), copyright)
        )

        warning = options.fonts["MedievalSharp-xOZ5"]["20"].render(
            "Warning; This game may contain Michael Bay", 1, (0, 0, 0)
        )
        self.images.append(
            ((30, 1080 - warning.get_size()[1]), warning)
        )

        marcel = pg.image.load("assets/images/marcel.png").convert_alpha()
        self.images.append(
            ((1920 / 4 - marcel.get_size()[0] / 2, 1080 * 3 / 4 - marcel.get_size()[1] / 2), marcel)
        )
        flipped = pg.transform.flip(marcel, True, False)
        self.images.append(
            ((1920 * 3 / 4 - flipped.get_size()[0] / 2, 1080 * 3 / 4 - flipped.get_size()[1] / 2), flipped)
        )

    def loop(self):
        super().loop()
        self.total_time += self.screen.elapsed_time

        self.update()
        self.handleEvents()

        self.draw()
        self.screen.flip()

    def update(self):
        """Updates the menu parts that do not depend on the user input"""

        if self.total_time >= 2.55 and self.percussion[0] == 0:
            self.percussion = (1, None)  # Functions.Percu(20, 297))
        if self.total_time >= 5.45 and self.percussion[0] == 1:
            self.percussion = (2, None)  # Functions.Percu(20, 297))
        if self.total_time >= 8.5 and self.percussion[0] == 2:
            self.percussion = (3, None)  # Functions.Percu(20, 297))

    def _draw(self):
        if self.total_time >= 11.7 and self.total_time < 12.2:
            self.show_buttons = False
            self.background.fill((0, 0, 0))
            self.screen.blit(self.background, (0, 0))
        elif self.total_time >= 12.1 and self.total_time <= 23.7:
            self.show_buttons = True

            self.background.fill((
                random.randrange(255),
                random.randrange(255),
                random.randrange(255)
                )
            )
            self.draw_normal_menu()
        else:
            self.draw_normal_menu()

    def draw_normal_menu(self):
        self.screen.blit(self.background, (0, 0))
        for position, image in self.images:
            self.screen.blit(image, position)

    def handleEvents(self):
        for event in super().handleEvent():
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.running = False
            elif event.type == pg.QUIT:
                self.running = False
    
    def launch(self, toLaunch: str):
        if toLaunch == "quit":
            self.running = False
        elif toLaunch == "game":
            GameIntro(self.screen)()
        print(f"Launching: {toLaunch}")
