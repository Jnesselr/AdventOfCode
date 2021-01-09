from aoc.util.coordinate import Coordinate, CoordinateSystem
from aoc.util.grid import MagicGrid
from aoc.util.inputs import Input


class Y2016D13(object):
    def __init__(self, file_name):
        self.favorite_number = Input(file_name).int()

        def _grid(_: MagicGrid[bool], coordinate: Coordinate) -> bool:
            x = coordinate.x
            y = coordinate.y

            if x < 0 or y < 0:
                return False

            result = x*x + 3*x + 2*x*y + y + y*y
            result += self.favorite_number

            return bin(result).count("1") % 2 == 0

        self.grid = MagicGrid[bool](_grid)
        self.start = Coordinate(1, 1, system=CoordinateSystem.X_RIGHT_Y_DOWN)

    def part1(self):
        end = Coordinate(31, 39, system=CoordinateSystem.X_RIGHT_Y_DOWN)

        path = self.grid.find_path(self.start, end, True)

        result = len(path) - 1

        print("Part 1:", result)

    def part2(self):
        flood_map = self.grid.flood_map(self.start, True, max_value=50)
        result = len(flood_map)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2016D13("2016/13.txt")
    code.part1()
    code.part2()
