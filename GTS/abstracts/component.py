import pygame as pg

from GTS.animations.image_animation import ImageAnimation
from GTS.animations.movement_animation import MovementAnimation


class Component:
    def __init__(self,
        name: str,
        image: pg.Surface,
        movement_animation: MovementAnimation = None,
        image_animation: ImageAnimation = None
    ):
        self.name = name

        self.movement_path = None

        self.animation_speed = None

        self.image_animation: ImageAnimation = None

    def update(self):
        pass

    def draw(self, screen: pg.Surface):
        pass

    def set_movement_path(self, path: list):
        self.movement_path = path

    def set_animation_speed(self, speed: int):
        self.animation_speed = speed
    
    def set_image_animation(self, path: str, speed: int):
        self.image_animation = ImageAnimation(path, speed)
    
    def set_animation(self, animation: Animation):
        self.animation = animation

    def __str__(self):
        return f"Component({self.name})"
