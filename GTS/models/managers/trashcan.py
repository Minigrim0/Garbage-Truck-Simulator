import random
import copy

import pygame as pg

from GTS.models.components.trashcan import TrashCan
from GTS.models.gts import GarbageTruckSimulator
from GTS.models.truck import Truck
from GTS.utils.bound import bound
from GTS.animations.sprite_animation import SpriteAnimation


class TrashCanManager:
    MIN_HEIGHT = 350
    MAX_HEIGHT = 620
    SPAWN_MIN_OFFSET = 30
    SPAWN_MAX_OFFSET = 60

    instance = None

    @staticmethod
    def getInstance(*args, **kwargs):
        if TrashCanManager.instance is None:
            TrashCanManager.instance = TrashCanManager(*args, **kwargs)
        return TrashCanManager.instance

    def __init__(self):
        if TrashCanManager.instance is not None:
            raise Exception("This class is a singleton!")
        TrashCanManager.instance = self

        self.trashcans: list = []
        self.explosions: list = []
        self.direction = None

        self.trashcan_spawn_cooldown = 0.5
        self.spawns_before_direction_change = 5

        self.time_since_last_trashcan_spawn = 0

        self.game_instance = GarbageTruckSimulator.getInstance()
        self.game_instance.options.load_sound("assets/sounds/trashcan/trashcan_explode.ogg", "trashcan_explode")
        self.trashcan_image : pg.Surface = pg.image.load("assets/images/poubelle.png").convert_alpha()
        self.trashcan_death_sound = "trashcan_explode"

        self.trashcan_explosion_animation: SpriteAnimation = SpriteAnimation(
            "assets/images/animations/explosions/small_explosion/", callback=self._remove_animation, speed=15
        )

    def _remove_animation(self):
        self.explosions = self.explosions[1:]

    def _spawn_trashcan(self):
        """Spawns a new trashcan in the vicinity of the last one spawned"""
        height = self.trashcans[-1].heigth if self.trashcans else TrashCanManager.MIN_HEIGHT + (TrashCanManager.MAX_HEIGHT - TrashCanManager.MIN_HEIGHT) / 2
        if self.direction is None or len(self.trashcans) % self.spawns_before_direction_change == 0:
            self.direction = random.choice([-1, 1])
            self.direction = self.direction * random.randint(TrashCanManager.SPAWN_MIN_OFFSET, TrashCanManager.SPAWN_MAX_OFFSET)
        height += self.direction
        height = bound(TrashCanManager.MIN_HEIGHT, TrashCanManager.MAX_HEIGHT, height)
        self.trashcans.append(TrashCan((1920, height), self.trashcan_image))

    def update(self, timeElapsed: float, truck: Truck):
        self.time_since_last_trashcan_spawn += timeElapsed
        if self.time_since_last_trashcan_spawn > self.trashcan_spawn_cooldown:
            self.time_since_last_trashcan_spawn = 0
            self._spawn_trashcan()

        for can in self.trashcans:
            if not can.update(timeElapsed, truck):
                self.game_instance.options.play_sound(self.trashcan_death_sound)
                self.trashcans.remove(can)
                self.explosions.append(copy.copy(self.trashcan_explosion_animation))
                self.explosions[-1].setPosition(can.position)
                self.explosions[-1].play()

        for explosion in self.explosions:
            explosion.update(timeElapsed)
            explosion.move((- truck.actual_speed * timeElapsed, 0))

    def draw(self, screen):
        for trashcan in self.trashcans:
            trashcan.draw(screen)

        for explosion in self.explosions:
            explosion.draw(screen, explosion)
