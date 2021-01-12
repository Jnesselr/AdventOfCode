import re
from typing import Dict, Tuple

from aoc.util.inputs import Input


class Y2015D6(object):
    def __init__(self, file_name):
        self.lines = Input(file_name).lines()

        self.bool_grid: Dict[Tuple[int, int], bool] = {}
        self.int_grid: Dict[Tuple[int, int], int] = {}

        for line in self.lines:
            if line.startswith("turn on"):
                for x, y in self._range(line):
                    self.bool_grid[x, y] = True
                    self.int_grid[x, y] = self.int_grid.setdefault((x, y), 0) + 1
            elif line.startswith("turn off"):
                for x, y in self._range(line):
                    self.bool_grid[x, y] = False
                    self.int_grid[x, y] = max(self.int_grid.setdefault((x, y), 0) - 1, 0)
            elif line.startswith("toggle"):
                for x, y in self._range(line):
                    self.bool_grid[x, y] = not self.bool_grid.setdefault((x, y), False)
                    self.int_grid[x, y] = self.int_grid.setdefault((x, y), 0) + 2

    def part1(self):
        result = sum(1 for value in self.bool_grid.values() if value)

        print("Part 1:", result)

    def part2(self):
        result = sum(value for value in self.int_grid.values())

        print("Part 2:", result)

    @staticmethod
    def _range(line):
        search = re.search(r'(\d+),(\d+) through (\d+),(\d+)', line)
        x1 = int(search.group(1))
        y1 = int(search.group(2))
        x2 = int(search.group(3))
        y2 = int(search.group(4))

        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                yield x, y


if __name__ == '__main__':
    code = Y2015D6("2015/6.txt")
    code.part1()
    code.part2()
