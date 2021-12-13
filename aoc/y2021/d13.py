import re

from aoc.util.coordinate import Coordinate
from aoc.util.grid import InfiniteGrid, Grid
from aoc.util.inputs import Input


class Y2021D13(object):
    fold_regex = re.compile(r'fold along ([xy])=(\d+)')

    def __init__(self, file_name):
        grid: InfiniteGrid[str] = InfiniteGrid[str]()

        dot_coordinates, folds = Input(file_name).grouped()

        line: str
        for line in dot_coordinates:
            x, y = line.split(',')
            grid[x, y] = '#'

        self._points_after_one = 0

        for index, fold in enumerate(folds):
            match = self.fold_regex.match(fold)

            new_grid = InfiniteGrid[str]()

            axis = match.group(1)
            value = int(match.group(2))

            if axis == 'y':
                def fold_func(coordinate: Coordinate):
                    if coordinate.y > value:
                        return Coordinate(
                            x=coordinate.x,
                            y=-(coordinate.y - value) + value,
                            system=coordinate.system
                        )
                    else:
                        return coordinate
            else:
                def fold_func(coordinate: Coordinate):
                    if coordinate.x > value:
                        return Coordinate(
                            x=-(coordinate.x - value) + value,
                            y=coordinate.y,
                            system=coordinate.system
                        )
                    else:
                        return coordinate

            for c, v in grid.items():
                new_grid[fold_func(c)] = v

            grid = new_grid

            if index == 0:
                self._points_after_one = len(grid.items())

        self.grid: Grid[str] = grid.to_grid()

    def part1(self):
        result = self._points_after_one

        print("Part 1:", result)

    def part2(self):
        print("Part 2:")

        self.grid.print(not_found=' ')


if __name__ == '__main__':
    code = Y2021D13("2021/13.txt")
    code.part1()
    code.part2()
