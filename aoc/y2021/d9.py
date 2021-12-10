import math
from typing import List

from aoc.util.coordinate import Coordinate
from aoc.util.grid import InfiniteGrid
from aoc.util.inputs import Input


class Y2021D9(object):
    def __init__(self, file_name):
        self._grid: InfiniteGrid[int] = Input(file_name).grid().map(lambda x: int(x))
        self._low_points: List[Coordinate] = []

        coordinate: Coordinate
        for coordinate, value in self._grid.items():
            neighbors = coordinate.neighbors()
            all_greater = True
            for neighbor in neighbors:
                if neighbor not in self._grid:
                    continue
                if self._grid[neighbor] <= value:
                    all_greater = False

            if all_greater:
                self._low_points.append(coordinate)

    def part1(self):
        result = 0

        for coordinate in self._low_points:
            result += self._grid[coordinate] + 1

        print("Part 1:", result)

    def part2(self):
        basin_sizes = []

        for low_point in self._low_points:
            basin_size = len(self._grid.flood_map(low_point, 0, 1, 2, 3, 4, 5, 6, 7, 8))
            basin_sizes.append(basin_size)

        basin_sizes = sorted(basin_sizes)[-3:]

        result = math.prod(basin_sizes)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2021D9("2021/9.txt")
    code.part1()
    code.part2()
