import bezier
import numpy as np


class MovingPoint:
    START_TO_END = 0
    END_TO_START = 1

    def __init__(self, start_pos: tuple, end_pos: tuple, time: float = 1.0):
        """
        Creates a new Movable Object, that will update its position
        following a linear path between the start and end positions

        The animation will take <time> seconds to complete.

        A bezier curve can be used instead of a linear path by
        calling the set_bezier method.

        Args:
            start_pos (tuple): The starting position of the object
            end_pos (tuple): The end position of the object
            time (float, optional): The time taken by the animation to be performed. Defaults to 1.0.
        """
        self.path = (start_pos, end_pos)
        self.current_position = start_pos

        self.allowed_time = time
        self.animation_time = 0

        self.bezier = None
        self.moving_to_start = False

        self.direction = Movable.START_TO_END

    @property
    def x(self):
        return self.current_position[0]

    @property
    def y(self):
        return self.current_position[1]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"MovingPoint({self.current_position}, {self.path}, {self.allowed_time})"

    def update(self, delta_time: float):
        """Updates the object's position if it is moving"""

        self.animation_time += delta_time
        if self.bezier is None:
            advance = animation_time / self.allowed_time
        else:
            advance = self.bezier.evaluate(animation_time / self.allowed_time)[0][0]

        self.current_position = (
            self.path[self.direction][0] + (self.path[int(not bool(self.direction))][0] - self.path[self.direction][0]) * advance,
            self.path[self.direction][1] + (self.path[int(not bool(self.direction))][1] - self.path[self.direction][1]) * advance
        )

    def set_bezier_movement(self, control_points: list):
        """Sets the bezier curve to be used for the speed on the linear path"""

        if len(control_points) < 2:
            raise RuntimeError("At least 2 control points are required")
        if control_points[0] != (0, 0) or control_points[-1] != (1, 1):
            raise RuntimeError("The first control point must be (0, 0) and the last must be (1, 1)")

        nodes = [[], []]
        for point in control_points:
            nodes[0].append(point[0])
            nodes[1].append(point[1])

        nodes = np.asfortranarray(nodes)
        self.bezier = bezier.Curve.from_nodes(nodes)
