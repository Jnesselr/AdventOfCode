import enum

from aoc.util.coordinate import Coordinate
from aoc.util.grid import Grid
from aoc.util.inputs import Input


class Moving(enum.Enum):
    EAST = enum.auto()
    SOUTH = enum.auto()


class Y2021D25(object):
    def __init__(self, file_name):
        self._grid = Input(file_name).grid()

    def part1(self):
        result = 0

        grid = self._grid.copy()

        while True:
            result += 1
            changed_east, grid = self._mutate(grid, Moving.EAST)
            changed_south, grid = self._mutate(grid, Moving.SOUTH)
            # grid.print()
            # print()

            if not changed_east and not changed_south:
                break

        print("Part 1:", result)

    @staticmethod
    def _mutate(grid: Grid[str], moving: Moving) -> (bool, Grid[str]):
        result = grid.copy()
        max_x = grid.max_x
        max_y = grid.max_y

        locations = grid.find('>') if moving == Moving.EAST else grid.find('v')
        something_changed = False

        for location in locations:
            test = location.right() if moving == Moving.EAST else location.down()
            if test.x > max_x:
                test = Coordinate(0, test.y, system=test.system)
            if test.y > max_y:
                test = Coordinate(test.x, 0, system=test.system)

            if grid[test] == '.':
                result[test] = '>' if moving == Moving.EAST else 'v'
                result[location] = '.'
                something_changed = True

        return something_changed, result


if __name__ == '__main__':
    code = Y2021D25("2021/25.txt")
    code.part1()
