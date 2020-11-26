from typing import Set

from aoc.util.coordinate import Coordinate, CoordinateSystem, BoundingBox
from aoc.util.grid import InfiniteGrid
from aoc.util.inputs import Input


class Y2018D6(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.coordinates: Set[Coordinate] = set()
        self.grid = InfiniteGrid[Coordinate]()

        for line in lines:
            x, y = line.split(', ')
            coordinate = Coordinate(int(x), int(y), system=CoordinateSystem.X_RIGHT_Y_DOWN)
            self.coordinates.add(coordinate)
            self.grid[coordinate] = coordinate

        self.bounding_box: BoundingBox = self.grid.bounding_box

        for x, y in self.bounding_box:
            test_coordinate = Coordinate(x, y, system=CoordinateSystem.X_RIGHT_Y_DOWN)

            distances = dict((coordinate, test_coordinate.manhattan(coordinate)) for coordinate in self.coordinates)
            _, min_distance = min(distances.items(), key=lambda i: i[1])
            min_coordinates = [coordinate for coordinate, distance in distances.items() if distance == min_distance]

            if len(min_coordinates) != 1:
                continue

            self.grid[test_coordinate] = min_coordinates[0]

    def part1(self):
        excluded_coordinates: Set[Coordinate] = set()

        for x in range(self.bounding_box.min_x, self.bounding_box.max_x + 1):
            coordinate = Coordinate(x, self.bounding_box.min_y, system=CoordinateSystem.X_RIGHT_Y_DOWN)
            value = self.grid[coordinate]
            if value is not None:
                excluded_coordinates.add(value)

            coordinate = Coordinate(x, self.bounding_box.max_y, system=CoordinateSystem.X_RIGHT_Y_DOWN)
            value = self.grid[coordinate]
            if value is not None:
                excluded_coordinates.add(value)

        for y in range(self.bounding_box.min_y, self.bounding_box.max_y + 1):
            coordinate = Coordinate(self.bounding_box.min_x, y, system=CoordinateSystem.X_RIGHT_Y_DOWN)
            value = self.grid[coordinate]
            if value is not None:
                excluded_coordinates.add(value)

            coordinate = Coordinate(self.bounding_box.max_x, y, system=CoordinateSystem.X_RIGHT_Y_DOWN)
            value = self.grid[coordinate]
            if value is not None:
                excluded_coordinates.add(value)

        result = 0

        for coordinate in self.coordinates:
            if coordinate in excluded_coordinates:
                continue

            result = max(result, len(self.grid.find(coordinate)))

        print("Part 1:", result)

    def part2(self):
        result = 0

        for x, y in self.bounding_box:
            coordinate = Coordinate(x, y, system=CoordinateSystem.X_RIGHT_Y_DOWN)
            total_distance = sum(coordinate.manhattan(i) for i in self.coordinates)

            if total_distance < 10000:
                result += 1

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2018D6("2018/6.txt")
    code.part1()
    code.part2()
