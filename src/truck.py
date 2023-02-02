import math
import logging
import pygame as pg

from src.utils.rot_center import rot_center
from models.gts import GarbageTruckSimulator

from src.utils.bound import bound
from UI.components.loading_bar import LoadingBar
from src.animations.sprite_animation import SpriteAnimation

from UI.components.gauge import Gauge


class Truck(object):
    NONE = 0
    UP = 1
    DOWN = 2

    def __init__(self):
        self.image: pg.Surface = None

        self.nitro_level = 0
        self.nitro = False
        self.nitro_level = 0
        self.nitro_animation: SpriteAnimation = None
        self.ui_font = GarbageTruckSimulator.getInstance().options.fonts["MedievalSharp-xOZ5"]["20"]
        self.nitro_cooldown = 0
        self.nitro_replenish_speed = 5  # per second
        self.nitro_consumption_speed = 20  # per second
        self.nitro_gauge: Gauge = None
        self.nitro_multiplier = 2

        self.position = (15, 500)
        self.health = 100
        self.max_health = 100

        self._speed = 30  # km/h
        self.steering_speed = 250  # px/s
        self.steering = Truck.NONE
        self.speed_gauge: Gauge = None

        self.rotation = 0
        self.rotation_percent = 0

        self.health_bar: LoadingBar = None

        self.sounds: dict = {}

    @property
    def actual_speed(self):
        """
        Returns the truck speed in terms of pixels per second
        A meter is 64 pixels
        """
        return (self.speed / 3.6) * 64

    @property
    def speed(self):
        if self.nitro:
            return self._speed * self.nitro_multiplier
        return self._speed

    @property
    def alive(self):
        return self.health > 0

    def set_speed(self, speed: float):
        """Sets the speed of the truck (In km/h)

        Args:
            speed (float): The speed in km/h
        """
        self._speed = speed

    def load(self):
        logging.info("Loading truck")
        self.image = pg.image.load("assets/images/CamionPoubelle.png").convert_alpha()

        self.health_bar = LoadingBar(
            (0, 0),
            (self.image.get_width(), 10),
            max_val=self.max_health, initial_val=self.max_health,
            animation_type="linear", speed=50
        )

        self.nitro_animation = SpriteAnimation(
            "assets/images/animations/flames/", speed=15,
            rotation=90, loop=-1
        )
        self.nitro_animation.play()

        self.sounds["nitro"] = pg.mixer.Sound("assets/sounds/truck/nitro.ogg")

        self.nitro_gauge = Gauge(
            min_angle=-20, max_angle=200, min_value=0, max_value=100,
            initial_value=0, show_value=True, value_font=self.ui_font,
            value_color=(0, 0, 0), value_in_percent=True
        )

        self.speed_gauge = Gauge(
            min_angle=-20, max_angle=200, min_value=0, max_value=350,
            initial_value=self.speed, show_value=True, value_font=self.ui_font,
            value_color=(0, 0, 0), value_in_percent=False, value_suffix=" km/h"
        )

    def draw(self, screen):
        self.health_bar.draw(screen, self.position)
        screen.blit(
            rot_center(self.image, 5 * math.sin(2 * math.pi * self.rotation_percent)),
            self.position
        )
        self.nitro_gauge.draw(screen, (10, 800))
        self.speed_gauge.draw(screen, (250, 800))

        if self.nitro:
            self.nitro_animation.draw(screen, self.position)

    def hurt(self, damage):
        self.health -= damage

    def heal(self, heal):
        self.health += heal

    def _update_nitro(self, timeElapsed: float):
        if self.nitro_cooldown > 0:
            self.nitro_cooldown -= timeElapsed
        elif self.nitro:
            self.nitro_level = bound(0, 100, self.nitro_level - timeElapsed * self.nitro_consumption_speed)
            self.nitro_animation.update(timeElapsed)
            if self.nitro_level == 0:
                self.nitro = False
                self.nitro_cooldown = 5
                self.nitro_animation.reset()
        elif self.nitro_level < 100:
            self.nitro_level = bound(0, 100, self.nitro_level + timeElapsed * self.nitro_replenish_speed)

        self.nitro_level = round(self.nitro_level, 2)
        self.nitro_gauge.update(self.nitro_level)

    def update(self, timeElapsed: float):
        if self.steering != Truck.NONE:
            self.move(self.steering == Truck.UP, timeElapsed)
        self.health_bar.update(timeElapsed)
        self._update_nitro(timeElapsed)
        self.speed_gauge.update(self.speed)
        self.rotation_percent = bound(0, 1, self.rotation_percent + timeElapsed)
        if self.rotation_percent == 1:
            self.rotation_percent = 0

    def move(self, up: bool, timeElapsed: float):
        if up:
            self.position = (
                self.position[0],
                bound(350, 620, self.position[1] - self.steering_speed * timeElapsed),
            )
        else:
            self.position = (
                self.position[0],
                bound(350, 620, self.position[1] + self.steering_speed * timeElapsed),
            )

    def handleEvents(self, event):
        self.steering = Truck.NONE

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_DOWN:
                self.steering = Truck.DOWN
            elif event.key == pg.K_UP:
                self.steering = Truck.UP
            elif event.key == pg.K_RIGHT:
                if not self.nitro and self.nitro_cooldown <= 0 and self.nitro_level > 20:
                    self.sounds["nitro"].play()
                    self.nitro_animation.play()
                    self.nitro = True
