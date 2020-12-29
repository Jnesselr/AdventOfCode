from aoc.util.coordinate import Coordinate
from aoc.util.inputs import Input


class Y2019D3(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.line_a = self._to_coordinates(lines[0])
        self.line_b = self._to_coordinates(lines[1])

        self.intersections = set(self.line_a).intersection(set(self.line_b))

    @staticmethod
    def _to_coordinates(line_string):
        line = line_string.split(',')
        current: Coordinate = Coordinate(0, 0)
        coordinates = []

        for element in line:
            direction = element[0]
            count = int(element[1:])

            for _ in range(count):
                current = current.move(direction)
                coordinates.append(current)

        return coordinates

    def part1(self):
        result = min(self.intersections, key=lambda coord: coord.x + coord.y)

        print("Part 1:", result.x + result.y)

    def part2(self):
        result = len(self.line_a) + len(self.line_b)

        for intersection in self.intersections:
            index_a = self.line_a.index(intersection)
            index_b = self.line_b.index(intersection)

            total = index_a + index_b
            if total < result:
                result = total

        # The +2 is because we don't include the index in either list
        print("Part 2:", result + 2)


if __name__ == '__main__':
    code = Y2019D3("2019/3.txt")
    code.part1()
    code.part2()
