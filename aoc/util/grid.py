from __future__ import annotations
from typing import TypeVar, Generic

from aoc.util.coordinate import Coordinate, CoordinateSystem

T = TypeVar('T')


class InfiniteGrid(Generic[T]):
    def __init__(self):
        self._data = {}
        
    def clear(self):
        self._data = {}

    @staticmethod
    def _to_coordinate(position) -> Coordinate:
        """
        We make the assumption that the grid is x right y down if they're just passing in coordinates. However, the
        user can use any coordinate system they want in an infinite grid.
        """
        if isinstance(position, tuple):
            x, y = position
            position = Coordinate(x, y, system=CoordinateSystem.X_RIGHT_Y_DOWN)
        return position

    @property
    def max_x(self):
        return max(map(lambda coord: coord.x, self._data.keys()))

    @property
    def min_x(self):
        return min(map(lambda coord: coord.x, self._data.keys()))

    @property
    def max_y(self):
        return max(map(lambda coord: coord.y, self._data.keys()))

    @property
    def min_y(self):
        return min(map(lambda coord: coord.y, self._data.keys()))

    # TODO This makes assumptions about the coordinate system. It assumes X_RIGHT_Y_UP.
    def to_grid(self) -> Grid[T]:
        data = {}

        min_x = min_y = 4294967296
        max_x = max_y = 0

        for coordinate, item in self._data.items():
            x = coordinate.x
            y = coordinate.y
            if coordinate.system == CoordinateSystem.X_RIGHT_Y_DOWN:
                y = -y

            coordinate = Coordinate(x, y, system=CoordinateSystem.X_RIGHT_Y_UP)
            data[coordinate] = item

            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)

        width = max_x - min_x + 1
        height = max_y - min_y + 1

        result = Grid[T](width, height)
        for coordinate, item in data.items():
            result[coordinate.x - min_x, max_y - coordinate.y] = item

        return result

    def __getitem__(self, position):
        position = self._to_coordinate(position)

        if position in self._data:
            return self._data[position]
        return None

    def __setitem__(self, position, item):
        position = self._to_coordinate(position)

        self._data[position] = item

    def __contains__(self, position):
        position = self._to_coordinate(position)

        return position in self._data

    def find(self, test):
        result = []

        for coordinate, item in self._data.items():
            if callable(test):
                if test(item):
                    result.append(coordinate)
            elif item == test:
                result.append(coordinate)

        return result


# TODO Add constraints for setting/getting position to be in bounds
class Grid(InfiniteGrid[T]):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height

    def fill(self, item: T):
        for row in range(self.height):
            for col in range(self.width):
                coordinate = Coordinate(col, row, system=CoordinateSystem.X_RIGHT_Y_DOWN)

                self._data[coordinate] = item

    # TODO Add a key function for items that aren't characters
    # TODO Add a default character to use if the coordinate isn't in there
    def print(self, key=None, not_found=' '):
        if key is None:
            def key(item):
                return item[0]

        for row in range(self.height):
            line = ""
            for col in range(self.width):
                coordinate = Coordinate(col, row, system=CoordinateSystem.X_RIGHT_Y_DOWN)

                if coordinate in self._data:
                    line += key(self._data[coordinate])
                else:
                    line += not_found

            print(line)
