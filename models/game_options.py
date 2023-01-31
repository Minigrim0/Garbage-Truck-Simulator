import glob
import json
import os

import pygame as pg

from src.utils.bound import bound


class GameOptions:
    """The options of the ongoing game"""

    instance = None

    @staticmethod
    def getInstance():
        """Returns the model's instance, creating it if needed"""
        if GameOptions.instance is None:
            GameOptions()
        return GameOptions.instance

    def __init__(self):
        if GameOptions.instance is not None:
            raise RuntimeError("Trying to instanciate a second object of a singleton class")
        GameOptions.instance = self

        self.volume = 5
        self.musics = {}

        self.fonts = {}

        self._load()

    def __getitem__(self, category: str) -> dict:
        if category not in self.settings.keys():
            return None
        return self.settings[category]

    def _load(self):
        """Loads the game's fonts"""
        for font in glob.glob("UI/assets/fonts/*/*.ttf"):
            filename = os.path.splitext(os.path.split(font)[1])[0]
            self.fonts[filename] = {}
            for size in [12, 14, 20, 25, 35, 40, 60, 100]:
                self.fonts[filename][str(size)] = pg.font.Font(font, size)

        with open("assets/settings.json") as settings:
            self.settings = json.load(settings)

        for music in glob.glob("assets/musics/*.ogg"):
            music_name = os.path.splitext(os.path.split(music)[1])[0]
            self.musics[music_name] = pg.mixer.Sound(music)

    def fullPath(self, category, path):
        """Returns the concatenated full path for a category and a sub path"""
        return os.path.join(self["paths"][category], path)

    def changeVolume(self, value):
        """Modifies the volume options, and updates it in pygame (and makes sure it's in its bounds)"""
        self.volume += value
        self.volume = bound(0, 10, self.volume)
        pg.mixer.music.set_volume(self.volume / 10)
