import re
from dataclasses import dataclass
from typing import List

from aoc.util.coordinate import Coordinate
from aoc.util.grid import InfiniteGrid
from aoc.util.inputs import Input


@dataclass(frozen=True)
class Line(object):
    x1: int
    y1: int
    x2: int
    y2: int


class Y2021D5(object):
    line_regex = re.compile(r'(\d+),(\d+) -> (\d+),(\d+)')

    def __init__(self, file_name):
        lines = Input(file_name).lines()

        self._lines: List[Line] = []

        for line in lines:
            match = self.line_regex.match(line)
            line = Line(
                x1=int(match.group(1)),
                y1=int(match.group(2)),
                x2=int(match.group(3)),
                y2=int(match.group(4)),
            )
            self._lines.append(line)

    def part1(self):
        grid = InfiniteGrid[int]()

        for line in self._lines:
            if line.x1 != line.x2 and line.y1 != line.y2:
                continue

            if line.x1 == line.x2:
                min_y = min(line.y1, line.y2)
                max_y = max(line.y1, line.y2)
                for y in range(min_y, max_y + 1):
                    point = (line.x1, y)
                    if point not in grid:
                        grid[point] = 1
                    else:
                        grid[point] = grid[point] + 1
            elif line.y1 == line.y2:
                min_x = min(line.x1, line.x2)
                max_x = max(line.x1, line.x2)
                for x in range(min_x, max_x + 1):
                    point = (x, line.y1)
                    if point not in grid:
                        grid[point] = 1
                    else:
                        grid[point] = grid[point] + 1

        result = len(grid.find(lambda _: _ > 1))

        print("Part 1:", result)

    def part2(self):
        grid = InfiniteGrid[int]()

        for line in self._lines:
            if line.x1 == line.x2:
                min_y = min(line.y1, line.y2)
                max_y = max(line.y1, line.y2)
                for y in range(min_y, max_y + 1):
                    point = (line.x1, y)
                    if point not in grid:
                        grid[point] = 1
                    else:
                        grid[point] = grid[point] + 1
            elif line.y1 == line.y2:
                min_x = min(line.x1, line.x2)
                max_x = max(line.x1, line.x2)
                for x in range(min_x, max_x + 1):
                    point = (x, line.y1)
                    if point not in grid:
                        grid[point] = 1
                    else:
                        grid[point] = grid[point] + 1
            else:
                start_x = min(line.x1, line.x2)
                max_x = max(line.x1, line.x2)
                start_y = line.y1 if line.x1 == start_x else line.y2
                diff = max_x - start_x + 1
                slope = (line.y2 - line.y1) / (line.x2 - line.x1)

                for i in range(diff):
                    point = (start_x + i, start_y + i * slope)
                    if point not in grid:
                        grid[point] = 1
                    else:
                        grid[point] = grid[point] + 1

        result = len(grid.find(lambda _: _ > 1))

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2021D5("2021/5.txt")
    code.part1()
    code.part2()
