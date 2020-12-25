from aoc.util.coordinate import Coordinate
from aoc.util.inputs import Input


class Y2017D11(object):
    def __init__(self, file_name):
        line = Input(file_name).line()

        self.furthest_distance = 0
        self.coordinate = Coordinate(0, 0)
        for step in line.split(","):
            if step == 'n':
                self.coordinate = self.coordinate.up()
            elif step == 's':
                self.coordinate = self.coordinate.down()
            elif step == 'ne':
                self.coordinate = self.coordinate.right()
            elif step == 'sw':
                self.coordinate = self.coordinate.left()
            elif step == 'nw':
                self.coordinate = self.coordinate.left().up()
            elif step == 'se':
                self.coordinate = self.coordinate.right().down()

            self.furthest_distance = max(self.furthest_distance, self._distance(self.coordinate))

    @staticmethod
    def _distance(coordinate: Coordinate) -> int:
        if (coordinate.x < 0 < coordinate.y) or (coordinate.x > 0 > coordinate.y):
            return max(abs(coordinate.x), abs(coordinate.y))
        return abs(coordinate.x + coordinate.y)

    def part1(self):
        result = self._distance(self.coordinate)

        print("Part 1:", result)

    def part2(self):
        result = self.furthest_distance

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2017D11("2017/11.txt")
    code.part1()
    code.part2()
