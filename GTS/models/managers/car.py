import random
import copy
import pygame as pg

from GTS.models.truck import Truck
from GTS.models.gts import GarbageTruckSimulator
from GTS.models.components.car import Car

from GTS.animations.sprite_animation import SpriteAnimation


class CarManager:

    instance = None

    @staticmethod
    def getInstance():
        if CarManager.instance is None:
            CarManager()
        return CarManager.instance

    def __init__(self):
        if CarManager.instance is not None:
            raise RuntimeError("Trying to instanciate a second object of a singleton class")
        CarManager.instance = self

        self.cars = []
        self.explosions = []

        self.car_spawn_cooldown = 3
        self.spawns_before_direction_change = 5

        self.time_since_last_car_spawn = 0

        self.game_instance = GarbageTruckSimulator.getInstance()
        self.game_instance.options.load_sound("assets/sounds/car/car_explode.ogg", "car_explode", volume=2)
        self.car_image: pg.Surface = pg.image.load("assets/images/car.png").convert_alpha()
        self.car_death_sound: str = "car_explode"

        self.car_explosion_animation: SpriteAnimation = SpriteAnimation(
            "assets/images/animations/explosions/big_explosion/", callback=self._remove_animation, speed=15,
            image_size=(200, 200)
        )

    def _remove_animation(self):
        self.explosions = self.explosions[1:]

    def _spawn_car(self):
        spawn_position = random.randint(0, 2)
        car = Car(self.car_image, (1920, 375 + spawn_position * 150))
        self.cars.append(car)

    def update(self, delta_time: float, truck: Truck):
        self.time_since_last_car_spawn += delta_time

        if self.time_since_last_car_spawn >= self.car_spawn_cooldown:
            self.time_since_last_car_spawn = 0
            self._spawn_car()

        for car in self.cars:
            if not car.update(delta_time, truck):
                self.explosions.append(copy.copy(self.car_explosion_animation))
                self.explosions[-1].setPosition(
                    (
                        car.position[0] + self.car_image.get_width() - 200,
                        car.position[1] + self.car_image.get_height() - 200)
                )
                self.explosions[-1].play()
                self.game_instance.options.play_sound(self.car_death_sound)
                self.cars.remove(car)

        for explosion in self.explosions:
            explosion.update(delta_time)
            explosion.move((-truck.actual_speed * delta_time, 0))

    def draw(self, screen: pg.Surface):
        for car in self.cars:
            car.draw(screen)

        for explosion in self.explosions:
            explosion.draw(screen)
