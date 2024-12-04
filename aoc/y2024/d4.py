from collections import Counter

from aoc.util.coordinate import BoundingBox, Coordinate, CoordinateSystem
from aoc.util.inputs import Input


class Y2024D4(object):
    def __init__(self, file_name):
        self._grid = Input(file_name).grid()

    def part1(self):
        bounding_box: BoundingBox = self._grid.bounding_box
        c = Counter()

        for x in range(0, bounding_box.max_x + 1):
            for y in range(0, bounding_box.max_y + 1):
                coordinate = Coordinate(int(x), int(y), system=CoordinateSystem.X_RIGHT_Y_DOWN)

                if x <= bounding_box.max_x - 3:
                    right = self._grid[coordinate] + \
                            self._grid[coordinate.right()] + \
                            self._grid[coordinate.right(2)] + \
                            self._grid[coordinate.right(3)]

                    c[right] += 1

                if y <= bounding_box.max_y - 3:
                    down  = self._grid[coordinate] + \
                            self._grid[coordinate.down()] + \
                            self._grid[coordinate.down(2)] + \
                            self._grid[coordinate.down(3)]

                    c[down] += 1

                if x <= bounding_box.max_x - 3 and y <= bounding_box.max_y - 3:
                    right_down  = self._grid[coordinate] + \
                            self._grid[coordinate.right().down()] + \
                            self._grid[coordinate.right(2).down(2)] + \
                            self._grid[coordinate.right(3).down(3)]

                    c[right_down] += 1

                if x <= bounding_box.max_x - 3 and y >= 3:
                    right_up  = self._grid[coordinate] + \
                            self._grid[coordinate.right().up()] + \
                            self._grid[coordinate.right(2).up(2)] + \
                            self._grid[coordinate.right(3).up(3)]

                    c[right_up] += 1

        result = c["XMAS"] + c["SAMX"]

        print("Part 1:", result)

    def part2(self):
        bounding_box: BoundingBox = self._grid.bounding_box
        c = Counter()

        for x in range(1, bounding_box.max_x):
            for y in range(1, bounding_box.max_y):
                coordinate = Coordinate(int(x), int(y), system=CoordinateSystem.X_RIGHT_Y_DOWN)

                cross = self._grid[coordinate.left().up()] + \
                    self._grid[coordinate.right().up()] + \
                    self._grid[coordinate] + \
                    self._grid[coordinate.left().down()] + \
                    self._grid[coordinate.right().down()]

                c[cross] += 1

        result = c["MSAMS"] + c["MMASS"] + c["SSAMM"] + c["SMASM"]

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2024D4("2024/4.txt")
    code.part1()
    code.part2()
