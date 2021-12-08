from typing import List

from z3 import Int, Optimize, If

from aoc.util.inputs import Input
from aoc.util.search import MinSearch


def z3_abs(num):
    return If(num >= 0, num, -num)


class Y2021D7(object):
    def __init__(self, file_name):
        self._crabs: List[int] = Input(file_name).int_line()

    def part1(self):
        search = MinSearch(lambda i: sum([abs(x - i) for x in self._crabs]))
        result = search.test(search.min(0))

        print("Part 1:", result)

    def part2(self):
        search = MinSearch(lambda i: sum([(abs(x - i) * (abs(x - i) + 1)) // 2 for x in self._crabs]))
        result = search.test(search.min(0))

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2021D7("2021/7.txt")
    code.part1()
    code.part2()
