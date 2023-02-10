from GTS.models.screen import Screen

from GTS.animations.sprite_animation import SpriteAnimation
from GTS.animations.movement_animation import MovementAnimation


class Animation:
    def __init__(self, movement_animation: MovementAnimation = None, image_animation: SpriteAnimation = None):
        self.movement_animation: MovementAnimation = movement_animation
        self.image_animation: SpriteAnimation = image_animation

    def update(self, delta_time: float):
        if self.movement_animation is not None:
            self.movement_animation.update(delta_time)
        if self.image_animation is not None:
            self.image_animation.update(delta_time)

    def draw(self, screen: Screen, position: tuple):
        if self.image_animation is not None:
            self.image_animation.draw(screen, position)

    def __str__(self):
        return f"Animation({self.movement_animation}, {self.image_animation})"
