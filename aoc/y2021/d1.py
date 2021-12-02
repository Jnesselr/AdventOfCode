from typing import List

from aoc.util.inputs import Input


class Y2021D1(object):
    def __init__(self, file_name):
        self._input: List[int] = Input(file_name).ints()

    def part1(self):
        result = 0

        current = self._input[0]
        for item in self._input[1:]:
            if item > current:
                result += 1
            current = item

        print("Part 1:", result)

    def part2(self):
        result = 0

        input_length = len(self._input)
        for index in range(input_length - 3):
            first = second = 0
            first += self._input[index]
            first += self._input[index + 1]
            first += self._input[index + 2]
            second += self._input[index + 1]
            second += self._input[index + 2]
            second += self._input[index + 3]

            if second > first:
                result += 1

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2021D1("2021/1.txt")
    code.part1()
    code.part2()
