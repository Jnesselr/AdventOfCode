import itertools

from aoc.util.coordinate import Coordinate, CoordinateSystem
from aoc.util.grid import Grid
from aoc.util.inputs import Input


class Y2015D18(object):
    def __init__(self, file_name):
        self.initial_grid = Input(file_name).grid()

    def part1(self):
        grid = self.initial_grid

        for _ in range(100):
            grid = self._next(grid)

        result = len(grid.find('#'))

        print("Part 1:", result)

    def part2(self):
        grid = self.initial_grid

        for _ in range(100):
            grid = self._next(grid, lights_stuck=True)

        result = len(grid.find('#'))

        print("Part 2:", result)

    @staticmethod
    def _next(grid: Grid[str], lights_stuck=False) -> Grid[str]:
        result = grid.copy()

        for x, y in itertools.product(range(100), repeat=2):
            coordinate = Coordinate(x, y, system=CoordinateSystem.X_RIGHT_Y_DOWN)
            neighbors = sum(1 for c in coordinate.neighbors8() if grid[c] == '#')

            if grid[coordinate] == '#' and neighbors not in [2, 3]:
                result[coordinate] = '.'
            elif grid[coordinate] == '.' and neighbors == 3:
                result[coordinate] = '#'

        if lights_stuck:
            result[0, 0] = '#'
            result[0, 99] = '#'
            result[99, 0] = '#'
            result[99, 99] = '#'

        return result


if __name__ == '__main__':
    code = Y2015D18("2015/18.txt")
    code.part1()
    code.part2()
