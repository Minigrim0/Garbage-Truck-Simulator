class AnimationPath:
    """A path that an animation can follow."""
    def __init__(self, path: list = None):
        self.path: list = path

    def __str__(self):
        return f"AnimationPath({self.path})"
