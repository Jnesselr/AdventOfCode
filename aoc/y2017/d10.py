from typing import List

from aoc.util.inputs import Input
from aoc.y2017.knot_hash import KnotHash


class Y2017D10(object):
    def __init__(self, file_name):
        self.input = Input(file_name).line()

    def part1(self):
        circle: List[int] = list(range(256))
        circle_size = len(circle)

        current_position = 0
        skip_size = 0

        for length in self.input.split(','):
            length = int(length)
            for i in range(length // 2):
                from_index: int = (current_position + i) % circle_size
                to_index: int = (current_position + length - i - 1) % circle_size
                temp: int = circle[from_index]
                circle[from_index] = circle[to_index]
                circle[to_index] = temp

            current_position = (current_position + length + skip_size) % circle_size
            skip_size += 1

        result = circle[0] * circle[1]
        print("Part 1:", result)

    def part2(self):
        result = KnotHash(self.input).hex

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2017D10("2017/10.txt")
    code.part1()
    code.part2()
