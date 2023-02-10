class AnimationSpeed:
    """
    A simple animation speed abstract class that defines the interface for
    animation speed classes.
    """

    def get_percent_done(self, time: float) -> float:
        raise NotImplementedError()
