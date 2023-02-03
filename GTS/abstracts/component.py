import pygame as pg

from GTS.abstracts.animations.animations import Animation
from GTS.animations.sprite_animation import SpriteAnimation
from GTS.animations.movement_animation import MovementAnimation


class Component:
    def __init__(self,
        name: str,
        image: pg.Surface,
        movement_animation: MovementAnimation = None,
        image_animation: SpriteAnimation = None
    ):
        self.name = name

        self.movement_path = None
        self.animation_speed = None

        self.image_animation: ImageAnimation = None

    def update(self):
        pass

    def draw(self, screen: pg.Surface):
        pass

    def set_animation_speed(self, speed: int):
        self.animation_speed = speed

    def set_movement_path(self, animation: MovementAnimation):
        self.animation.set_movement_animation(animation)

    def set_image_animation(self, animation: SpriteAnimation):
        self.animation.set_sprite_animation(animation)

    def set_animation(self, animation: Animation):
        self.animation = animation

    def __str__(self):
        return f"Component({self.name})"
