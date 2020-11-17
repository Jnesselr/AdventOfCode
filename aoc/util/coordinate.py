from __future__ import annotations
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
        return Coordinate(self.x + self.system.dx, self.y, system=self.system)

    def left(self):
        return Coordinate(self.x - self.system.dx, self.y, system=self.system)

    def up(self):
        return Coordinate(self.x, self.y + self.system.dy, system=self.system)

    def down(self):
        return Coordinate(self.x, self.y - self.system.dy, system=self.system)

    def neighbors(self):
        return [self.up(), self.down(), self.left(), self.right()]


@dataclass(frozen=True)
class BoundingBox(object):
    min_x: int = 2**32
    min_y: int = 2**32
    max_x: int = -2**32
    max_y: int = -2**32

    def expand(self, *points: Coordinate) -> BoundingBox:
        min_x: int = self.min_x
        min_y: int = self.min_y
        max_x: int = self.max_x
        max_y: int = self.max_y

        for point in points:
            min_x = min(min_x, point.x)
            max_x = max(max_x, point.x)
            min_y = min(min_y, point.y)
            max_y = max(max_y, point.y)

        return BoundingBox(min_x, min_y, max_x, max_y)

    def __contains__(self, item: Coordinate) -> bool:
        if item.x < self.min_x or item.x > self.max_x:
            return False

        if item.y < self.min_y or item.y > self.max_y:
            return False

        return True

    def shrink(self, amount=1) -> BoundingBox:
        min_x = self.min_x + amount
        min_y = self.min_y + amount
        max_x = self.max_x - amount
        max_y = self.max_y - amount

        return BoundingBox(min_x, min_y, max_x, max_y)


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
