import re
from typing import Set

from aoc.util.grid import InfiniteGrid
from aoc.util.inputs import Input


class Y2018D3(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.grid: InfiniteGrid[Set[int]] = InfiniteGrid[Set[int]]()
        self.all_ids = set()

        for line in lines:
            matched = re.match(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)", line)
            _id = int(matched.group(1))
            left = int(matched.group(2))
            top = int(matched.group(3))
            width = int(matched.group(4))
            height = int(matched.group(5))
            self.all_ids.add(_id)

            for x in range(left, left+width):
                for y in range(top, top+height):
                    if self.grid[x, y] is None:
                        self.grid[x, y] = set()

                    self.grid[x, y].add(_id)

        self.overlapping_coordinates = self.grid.find(lambda i: len(i) >= 2)

    def part1(self):
        result = len(self.overlapping_coordinates)

        print("Part 1:", result)

    def part2(self):
        overlapping_ids = set()
        for coordinate in self.overlapping_coordinates:
            overlapping_ids = overlapping_ids.union(self.grid[coordinate])
        result = self.all_ids - overlapping_ids

        if len(result) != 1:
            raise ValueError("Didn't get one result!")

        print("Part 2:", result.pop())


if __name__ == '__main__':
    code = Y2018D3("2018/3.txt")
    code.part1()
    code.part2()
