import pickle
import glob
import os
import random

import pygame as pg

from GTS.utils.bound import bound


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

        self.musics = {}
        self.fonts = {}

        self.settings: dict = {}

        self._load()

    def __getitem__(self, category: str) -> dict:
        if category not in self.settings.keys():
            return None
        return self.settings[category]

    def _load_default_settings(self):
        self.settings = {
            "music": {
                "on": False,
                "volume": 5
            },
            "effects": {
                "on": False,
                "volume": 5
            },
            "game": {
                "speed": 1,
                "difficulty": 1
            },
            "language": "en"
        }
        with open("assets/settings.pkl", "wb") as settings:
            pickle.dump(self.settings, settings)

    def _load(self):
        """Loads the game's fonts"""
        for font in glob.glob("assets/fonts/*/*.ttf"):
            filename = os.path.splitext(os.path.split(font)[1])[0]
            self.fonts[filename] = {}
            for size in [12, 14, 20, 25, 35, 40, 60, 100, 500]:
                self.fonts[filename][str(size)] = pg.font.Font(font, size)

        try:
            with open("assets/settings.pkl", "rb") as settings:
                self.settings = pickle.load(settings)
        except FileNotFoundError:
            self._load_default_settings()

        for music in glob.glob("assets/musics/*.ogg"):
            music_name = os.path.splitext(os.path.split(music)[1])[0]
            self.musics[music_name] = pg.mixer.Sound(music)

    def change_volume(self, value):
        """Modifies the volume options, and updates it in pygame (and makes sure it's in its bounds)"""
        self.volume += value
        self.volume = bound(0, 10, self.volume)
        pg.mixer.music.set_volume(self.volume / 10)

    def play_music(self, song_name: str = None, force: bool = False):
        """Plays the given song"""
        try:
            if song_name is not None:
                self["music"]["on"] = True
                if song_name not in self.musics:
                    song_name = random.choice(list(self.musics.keys()))
            else:
                song_name = random.choice(list(self.musics.keys()))
        except IndexError:
            self["music"]["on"] = False
            return

        if self["music"]["on"]:
            if force or not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(self.musics[song_name])
                pygame.mixer.music.play()

    def stop_music(self):
        """Stops the current song"""
        self.music_on = False
        pygame.mixer.music.stop()
