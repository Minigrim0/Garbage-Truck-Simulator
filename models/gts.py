import os
import glob
import random

import pygame

from models.game_options import GameOptions
from models.screen import Screen
from UI.menus.main import MainMenu


class GarbageTruckSimulator:
    """The Game singleton object, used to start the game in itself"""

    instance = None

    @staticmethod
    def getInstance():
        """Returns the model's instance, creating it if needed"""
        if GarbageTruckSimulator.instance is None:
            GarbageTruckSimulator()
        return GarbageTruckSimulator.instance

        self.music_on = True

    def __init__(self):
        if GarbageTruckSimulator.instance is not None:
            raise RuntimeError("This class is a Singleton!")
        GarbageTruckSimulator.instance = self

        self.screen = Screen.getInstance((1920, 1080), "GarbageTruckSimulator", "UI/assets/images/icon.png", False)

        GameOptions.getInstance()

        self.songs = {}
        for song in glob.glob("assets/music/*.ogg"):
            song_name = os.path.splitext(os.path.basename(song))[0]
            self.songs[song_name] = song

        self.mainMenu = MainMenu(self.screen)

    def play_music(self, song_name: str):
        """Plays the given song"""
        if song_name not in self.songs:
            return
        pygame.mixer.music.load(self.songs[song_name])
        pygame.mixer.music.play()
        self.music_on = True

    def stop_music(self):
        """Stops the current song"""
        pygame.mixer.music.stop()
        self.music_on = False

    def playMusic(self):
        """Plays the next song if the current one is finished"""
        if self.music_on and not pygame.mixer.music.get_busy() and len(self.songs) > 0:
            pygame.mixer.music.load(self.songs[random.choice(list(self.songs.keys()))])
            pygame.mixer.music.play()

    def run(self):
        """Run the game by launching the main menu"""
        self.mainMenu()