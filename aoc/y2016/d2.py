from itertools import product

from aoc.util.coordinate import Coordinate, CoordinateSystem
from aoc.util.grid import Grid
from aoc.util.inputs import Input


class Y2016D2(object):
    def __init__(self, file_name):
        self.lines = Input(file_name).lines()

    def part1(self):
        keypad: Grid[str] = Grid[str](3, 3)
        for i, j in product(range(3), repeat=2):
            keypad[i, j] = str(3 * j + i + 1)

        result = self._get_keycode(keypad)

        print("Part 1:", result)

    def part2(self):
        keypad: Grid[str] = Grid[str](5, 5)
        keypad[2, 0] = "1"
        keypad[1, 1] = "2"
        keypad[2, 1] = "3"
        keypad[3, 1] = "4"
        keypad[0, 2] = "5"
        keypad[1, 2] = "6"
        keypad[2, 2] = "7"
        keypad[3, 2] = "8"
        keypad[4, 2] = "9"
        keypad[1, 3] = "A"
        keypad[2, 3] = "B"
        keypad[3, 3] = "C"
        keypad[2, 4] = "D"

        result = self._get_keycode(keypad)

        print("Part 2:", result)

    def _get_keycode(self, keypad: Grid[str]):
        coordinate = Coordinate(1, 1, system=CoordinateSystem.X_RIGHT_Y_DOWN)
        result = ""

        for line in self.lines:
            for character in line:
                new_coordinate = coordinate.move(character)
                if keypad[new_coordinate] is not None:
                    coordinate = new_coordinate
            result += keypad[coordinate]

        return result


if __name__ == '__main__':
    code = Y2016D2("2016/2.txt")
    code.part1()
    code.part2()
