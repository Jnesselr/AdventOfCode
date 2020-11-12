from typing import TypeVar, Generic

from aoc.util.coordinate import Coordinate, CoordinateSystem

T = TypeVar('T')


class Grid(Generic[T]):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._data = {}

    def fill(self, item: T):
        for row in range(self.height):
            for col in range(self.width):
                coordinate = Coordinate(col, row, system=CoordinateSystem.X_RIGHT_Y_DOWN)

                self._data[coordinate] = item

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

    # Todo Add a key function for items that aren't characters
    # Todo Add a default character to use if the coordinate isn't in there
    def print(self, not_found=' '):
        for row in range(self.height):
            line = ""
            for col in range(self.width):
                coordinate = Coordinate(col, row, system=CoordinateSystem.X_RIGHT_Y_DOWN)

                if coordinate in self._data:
                    line += self._data[coordinate][0]
                else:
                    print(not_found)

            print(line)

    def find(self, test):
        result = []

        for coordinate, item in self._data.items():
            if item == test:
                result.append(coordinate)

        return result

    def _to_coordinate(self, position) -> Coordinate:
        if isinstance(position, tuple):
            x, y = position
            position = Coordinate(x, y, system=CoordinateSystem.X_RIGHT_Y_DOWN)
        return position
