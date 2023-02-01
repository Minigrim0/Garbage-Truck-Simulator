from src.abstracts.animation.speed import AnimationSpeed


class MovementAnimation:
    """Combines a path and a speed to create an animation."""

    def __init__(self, path: list, speed: int):
        self.path = path
        self.speed: AnimationSpeed = speed
