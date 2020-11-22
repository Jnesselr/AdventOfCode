from typing import Set

from aoc.util.inputs import Input


class Y2018D1(object):
    def __init__(self, file_name):
        self.frequencies = list(map(lambda x: int(x), Input(file_name).lines()))

    def part1(self):
        result = sum(self.frequencies)

        print("Part 1:", result)

    def part2(self):
        result = 0
        seen: Set[int] = {0}

        should_continue = True
        while should_continue:
            for frequency in self.frequencies:
                result += frequency
                if result in seen:
                    should_continue = False
                    break
                else:
                    seen.add(result)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2018D1("2018/1.txt")
    code.part1()
    code.part2()
