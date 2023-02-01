import bezier
import numpy as np

from src.abstracts.animation.speed import AnimationSpeed


class BezierPath(AnimationPath):
    """
    Defines a path function from a bezier curve
    """

    def __init__(self, control_points: list):
        self.control_points = control_points
        self.curve: bezier.Curve = None

        self._build()

    def get_percent_done(self, time: float) -> float:
        """
        Returns the percentage of the animation that has been completed
        Time here is normalized between 0 and 1
        """
        return self.bezier.evaluate(time)[0][0]

    def _build(self):
        if len(self.control_points) < 2:
            raise RuntimeError("At least 2 control points are required")
        if self.control_points[0] != (0, 0) or self.control_points[-1] != (1, 1):
            raise RuntimeError("The first control point must be (0, 0) and the last must be (1, 1)")

        nodes = [[], []]
        for point in self.control_points:
            nodes[0].append(point[0])
            nodes[1].append(point[1])

        nodes = np.asfortranarray(nodes)
        self.bezier = bezier.Curve.from_nodes(nodes)