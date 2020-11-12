from dataclasses import dataclass
from enum import Enum, auto


class CoordinateSystem(Enum):
    """
    The notation for this is:
     +X is to the right
     -X is to the left
     +Y is up
     -Y is down

     Using a -1 in place of an axis negates that. So a -1 for dy in X_RIGHT_Y_DOWN means that "down" will subtract a
     negative 1 and therefore increase its value. That system is used for grids.
    """
    X_RIGHT_Y_UP = (1, 1)
    X_RIGHT_Y_DOWN = (1, -1)

    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy


@dataclass(frozen=True)
class Coordinate(object):
    x: int
    y: int
    system: CoordinateSystem = CoordinateSystem.X_RIGHT_Y_UP

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def right(self):
        return Coordinate(self.x + self.system.dx, self.y)

    def left(self):
        return Coordinate(self.x - self.system.dx, self.y)

    def up(self):
        return Coordinate(self.x, self.y + self.system.dy)

    def down(self):
        return Coordinate(self.x, self.y - self.system.dy)


class TurtleDirection(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

    def turn_right(self):
        if self == self.UP:
            return self.RIGHT
        elif self == self.RIGHT:
            return self.DOWN
        elif self == self.DOWN:
            return self.LEFT
        elif self == self.LEFT:
            return self.UP

    def turn_left(self):
        if self == self.UP:
            return self.LEFT
        elif self == self.LEFT:
            return self.DOWN
        elif self == self.DOWN:
            return self.RIGHT
        elif self == self.RIGHT:
            return self.UP


@dataclass(frozen=True)
class Turtle(object):
    direction: TurtleDirection
    coordinate: Coordinate = Coordinate(0, 0)

    def turn_left(self):
        return Turtle(direction=self.direction.turn_left(), coordinate=self.coordinate)

    def turn_right(self):
        return Turtle(direction=self.direction.turn_right(), coordinate=self.coordinate)

    def forward(self, count=1):
        result = self.coordinate
        for i in range(count):
            if self.direction == TurtleDirection.UP:
                result = result.up()
            elif self.direction == TurtleDirection.LEFT:
                result = result.left()
            elif self.direction == TurtleDirection.DOWN:
                result = result.down()
            elif self.direction == TurtleDirection.RIGHT:
                result = result.right()

        return Turtle(direction=self.direction, coordinate=result)
