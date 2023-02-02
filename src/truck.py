import math
import logging
import pygame as pg

# from src.utils.rot_center import rot_center
from src.utils.bound import bound
from UI.components.loading_bar import LoadingBar
from src.animations.sprite_animation import SpriteAnimation


class Truck(object):
    NONE = 0
    UP = 1
    DOWN = 2

    def __init__(self):
        self.image: pg.Surface = None

        self.nitro_level = 0
        self.nitro = False
        self.nitro_animation: SpriteAnimation = None

        self.position = (15, 500)
        self.health = 100
        self.max_health = 100
        self.speed = 30  # km/h
        self.steering_speed = 100  # px/s
        self.steering = Truck.NONE

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
    def alive(self):
        return self.health > 0

    def load(self):
        logging.info("Loading truck")
        self.image = pg.image.load("assets/images/CamionPoubelle.png").convert_alpha()

        self.health_bar = LoadingBar(
            (0, 0),
            (self.image.get_width(), 5),
            max_val=self.max_health, initial_val=self.max_health,
            animation_type="linear", speed=50
        )

        self.nitro_animation = SpriteAnimation(
            "assets/images/animations/flames/", speed=15,
            rotation=90, loop=-1
        )
        self.nitro_animation.play()

        self.sounds["nitro"] = pg.mixer.Sound("assets/sounds/truck/nitro.ogg")

    def draw(self, screen):
        self.health_bar.draw(screen, self.position)
        screen.blit(self.image, self.position)
        self.nitro_animation.draw(screen, self.position)

    def hurt(self, damage):
        self.health -= damage

    def heal(self, heal):
        self.health += heal

    def update(self, timeElapsed: float):
        if self.steering != Truck.NONE:
            self.move(self.steering == Truck.UP, timeElapsed)
        self.health_bar.update(timeElapsed)
        self.nitro_animation.update(timeElapsed)

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
                if not self.nitro:
                    self.sounds["nitro"].play()
                    self.nitro = True
