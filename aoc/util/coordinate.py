from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from typing import Iterator, Tuple


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

    def right(self, count=1) -> Coordinate:
        return Coordinate(self.x + self.system.dx * count, self.y, system=self.system)

    def left(self, count=1) -> Coordinate:
        return Coordinate(self.x - self.system.dx * count, self.y, system=self.system)

    def up(self, count=1) -> Coordinate:
        return Coordinate(self.x, self.y + self.system.dy * count, system=self.system)

    def down(self, count=1) -> Coordinate:
        return Coordinate(self.x, self.y - self.system.dy * count, system=self.system)

    def move(self, character) -> Coordinate:
        if character in 'R>':
            return self.right()
        elif character in 'L<':
            return self.left()
        elif character in 'U^':
            return self.up()
        elif character in 'DvV':
            return self.down()
        else:
            raise ValueError()

    def neighbors(self):
        return [self.up(), self.down(), self.left(), self.right()]

    def neighbors8(self):
        return [
            self.up(),
            self.down(),
            self.left(),
            self.right(),
            self.up().left(),
            self.up().right(),
            self.down().left(),
            self.down().right(),
        ]

    def manhattan(self, other: Coordinate):
        return abs(other.y - self.y) + abs(other.x - self.x)

    def cw_around(self, other: Coordinate, count=1):
        diff_coordinate = self - other
        for i in range(count):
            diff_coordinate = Coordinate(
                x=diff_coordinate.y,
                y=-diff_coordinate.x
            )
        return other + diff_coordinate

    def ccw_around(self, other: Coordinate, count=1):
        diff_coordinate = self - other
        for i in range(count):
            diff_coordinate = Coordinate(
                x=-diff_coordinate.y,
                y=diff_coordinate.x
            )
        return other + diff_coordinate

    def __lt__(self, other: Coordinate) -> bool:
        # Things are normally left to right, top to bottom
        return (self.y, self.x) < (other.y, other.x)

    def __mul__(self, other):
        if isinstance(other, Coordinate):
            return Coordinate(
                x=self.x * other.x,
                y=self.y * other.y
            )

        return Coordinate(self.x * other, self.y * other)

    def __add__(self, other):
        if isinstance(other, Coordinate):
            return Coordinate(
                x=self.x + other.x,
                y=self.y + other.y,
                system=self.system
            )

        return Coordinate(self.x + other, self.y + other)

    def __sub__(self, other):
        if isinstance(other, Coordinate):
            return Coordinate(
                x=self.x - other.x,
                y=self.y - other.y
            )

        return Coordinate(self.x - other, self.y - other)


@dataclass(frozen=True)
class BoundingBox(object):
    min_x: int = 2 ** 32
    min_y: int = 2 ** 32
    max_x: int = -2 ** 32
    max_y: int = -2 ** 32

    def expand_x(self, *x: int) -> BoundingBox:
        min_x: int = self.min_x
        max_x: int = self.max_x

        for value in x:
            min_x = min(min_x, value)
            max_x = max(max_x, value)

        return BoundingBox(min_x, self.min_y, max_x, self.max_y)

    def expand_y(self, *y: int) -> BoundingBox:
        min_y: int = self.min_y
        max_y: int = self.max_y

        for value in y:
            min_y = min(min_y, value)
            max_y = max(max_y, value)

        return BoundingBox(self.min_x, min_y, self.max_x, max_y)

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

    def __iter__(self) -> Iterator[Tuple[int, int]]:
        for x in range(self.min_x, self.max_x + 1):
            for y in range(self.min_y, self.max_y + 1):
                yield x, y

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

    def turn_left(self, count=1):
        direction = self.direction
        for i in range(count):
            direction = direction.turn_left()

        return Turtle(direction=direction, coordinate=self.coordinate)

    def turn_right(self, count=1):
        direction = self.direction
        for i in range(count):
            direction = direction.turn_right()

        return Turtle(direction=direction, coordinate=self.coordinate)

    def up(self, count=1):
        return Turtle(direction=self.direction, coordinate=self.coordinate.up(count))

    def down(self, count=1):
        return Turtle(direction=self.direction, coordinate=self.coordinate.down(count))

    def left(self, count=1):
        return Turtle(direction=self.direction, coordinate=self.coordinate.left(count))

    def right(self, count=1):
        return Turtle(direction=self.direction, coordinate=self.coordinate.right(count))

    def forward(self, count=1):
        coordinate = self.coordinate
        for i in range(count):
            coordinate = self.direction.move(coordinate)

        return Turtle(direction=self.direction, coordinate=coordinate)
