import pickle
import glob
import os
import random
import logging

import pygame as pg

from GTS.utils.bound import bound

logger = logging.getLogger("Game Options")

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

        self.musics: dict = {}
        self.sounds = {}
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
                "on": True,
                "volume": 5
            },
            "effects": {
                "on": True,
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

        for music in glob.glob("assets/music/*.ogg"):
            music_name = os.path.splitext(os.path.split(music)[1])[0]
            self.musics[music_name] = music
            logger.info(f"Loaded music {music_name}")

        pg.mixer.music.set_volume(self["music"]["volume"] / 10)

    def load_sound(self, path: str, sound_name: str, volume: int = -1):
        """Loads a sound from the assets folder"""
        if sound_name not in self.sounds.keys():
            self.sounds[sound_name] = pg.mixer.Sound(path)
            if volume >= 0:
                self.sounds[sound_name].set_volume(volume / 10)
            else:
                self.sounds[sound_name].set_volume(self["effects"]["volume"] / 10)

    def play_sound(self, sound_name: str):
        """Plays the given sound"""
        if self["effects"]["on"]:
            if sound_name in self.sounds.keys():
                self.sounds[sound_name].play()
            else:
                logger.warning(f"Trying to play a sound that doesn't exist {sound_name}")

    def change_music_volume(self, value):
        """Modifies the volume options, and updates it in pygame (and makes sure it's in its bounds)"""
        self["music"]["volume"] += value
        self["music"]["volume"] = bound(0, 10, self.volume)
        pg.mixer.music.set_volume(self["music"]["volume"] / 10)

    def change_effect_volume(self, value):
        """Modifies the volume options, and updates it in pygame (and makes sure it's in its bounds)"""
        self["effects"]["volume"] += value
        self["effects"]["volume"] = bound(0, 10, self.volume)
        for sound in self.sounds.values():
            sound.set_volume(self["effects"]["volume"] / 10)

    def play_music(self, song_name: str = None, force: bool = False):
        """Plays the given song"""
        try:
            if song_name is not None:
                self["music"]["on"] = True
                if song_name not in self.musics.keys():
                    song_name = random.choice(list(self.musics.keys()))
            else:
                song_name = random.choice(list(self.musics.keys()))
        except IndexError:
            self["music"]["on"] = False
            logger.warning(f"music {song_name} not found")
            return

        if self["music"]["on"]:
            if force or not pg.mixer.music.get_busy():
                pg.mixer.music.load(self.musics[song_name])
                pg.mixer.music.play()

    def stop_music(self):
        """Stops the current song"""
        self.music_on = False
        pg.mixer.music.stop()
