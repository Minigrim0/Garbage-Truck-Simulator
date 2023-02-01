from src.abstracts.animation.speed import AnimationSpeed
from src.abstracts.animation.path import AnimationPath


class MovementAnimation:
    """Combines a path and a speed to create an animation."""

    def __init__(self, path: AnimationPath = None, speed: AnimationSpeed = None):
        self.path: AnimationPath = path
        self.speed: AnimationSpeed = speed
