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

    def neighbors(self):
        return [self.up(), self.down(), self.left(), self.right()]


class TurtleDirection(Enum):
    UP = NORTH = auto()
    DOWN = SOUTH = auto()
    LEFT = WEST = auto()
    RIGHT = EAST = auto()

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

    def opposite(self):
        if self == self.UP:
            return self.DOWN
        elif self == self.DOWN:
            return self.UP
        elif self == self.LEFT:
            return self.RIGHT
        elif self == self.RIGHT:
            return self.LEFT

    def move(self, coordinate):
        if self == TurtleDirection.UP:
            return coordinate.up()
        elif self == TurtleDirection.LEFT:
            return coordinate.left()
        elif self == TurtleDirection.DOWN:
            return coordinate.down()
        elif self == TurtleDirection.RIGHT:
            return coordinate.right()


@dataclass(frozen=True)
class Turtle(object):
    direction: TurtleDirection
    coordinate: Coordinate = Coordinate(0, 0)

    def turn_left(self):
        return Turtle(direction=self.direction.turn_left(), coordinate=self.coordinate)

    def turn_right(self):
        return Turtle(direction=self.direction.turn_right(), coordinate=self.coordinate)

    def forward(self, count=1):
        coordinate = self.coordinate
        for i in range(count):
            coordinate = self.direction.move(coordinate)

        return Turtle(direction=self.direction, coordinate=coordinate)
