import bezier
import numpy as np

from src.abstracts.animation_speed import AnimationSpeed


class BezierSpeed(AnimationSpeed):
    """
    Defines a speed function from a bezier curve

    Curves must start at (0, 0) and end at (1, 1). The Y value of the curve
    is the percentage of the animation path that has been completed. The X axis
    is evaluated as the percentage of the animation time that has been completed.

    E.g. a linear curve would be [(0, 0), (1, 1)] and a curve that starts slow and
    ends fast would be [(0, 0), (1.0, 0.0), (1, 1)]
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