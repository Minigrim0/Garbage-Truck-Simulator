import os
import glob
import random

import pygame

from models.game_options import GameOptions
from models.screen import Screen


class GarbageTruckSimulator:
    """The Game singleton object, used to start the game in itself"""

    instance = None

    @staticmethod
    def getInstance():
        """Returns the model's instance, creating it if needed"""
        if GarbageTruckSimulator.instance is None:
            GarbageTruckSimulator()
        return GarbageTruckSimulator.instance

    def __init__(self):
        if GarbageTruckSimulator.instance is not None:
            raise RuntimeError("This class is a Singleton!")
        GarbageTruckSimulator.instance = self

        self.options = GameOptions.getInstance()
        self.screen = Screen.getInstance((1920, 1080), "GarbageTruckSimulator", "UI/assets/images/icon.png", False)

        from UI.menus.main import MainMenu

        self.mainMenu = MainMenu(self.screen)

    def __call__(self):
        """Run the game by launching the main menu"""
        self.mainMenu()
