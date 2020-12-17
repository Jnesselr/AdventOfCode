import itertools
from functools import reduce

from aoc.util.grid import Grid
from aoc.util.inputs import Input


class Y2020D17(object):
    def __init__(self, file_name):
        self.base_grid = Grid.from_str(Input(file_name).lines())

    def part1(self):
        result = self._get_sixth_cycle_count(3)

        print("Part 1:", result)

    def part2(self):
        result = self._get_sixth_cycle_count(4)

        print("Part 2:", result)

    def _get_sixth_cycle_count(self, dimensions):
        grid = set()

        for coordinate, item in self.base_grid.items():
            if item == '#':
                grid.add((coordinate.x, coordinate.y) + tuple([0]*(dimensions-2)))

        for i in range(6):
            grid = self._mutate(grid)

        return len(grid)

    def _mutate(self, grid):
        result = set()

        min_list = reduce(lambda acc, element: [min(x, y) for x, y in zip(acc, element)], grid)
        max_list = reduce(lambda acc, element: [max(x, y) for x, y in zip(acc, element)], grid)

        iterables = [list(range(x - 1, y + 2)) for x, y in zip(min_list, max_list)]

        for coordinate in itertools.product(*iterables):
            neighbor_count = self._neighbor_count(grid, coordinate)

            if coordinate in grid and 2 <= neighbor_count <= 3:
                result.add(coordinate)
            if coordinate not in grid and neighbor_count == 3:
                result.add(coordinate)

        return result

    @staticmethod
    def _neighbor_count(grid, coordinate):
        size = len(coordinate)
        result = 0
        for diff in itertools.product(range(-1, 2), repeat=size):
            new_coordinate = tuple(sum(x) for x in zip(diff, coordinate))
            if new_coordinate != coordinate and new_coordinate in grid:
                result += 1

        return result


if __name__ == '__main__':
    code = Y2020D17("2020/17.txt")
    code.part1()
    code.part2()
