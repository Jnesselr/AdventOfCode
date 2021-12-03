import re
from typing import List

from aoc.util.inputs import Input


class Y2021D2(object):
    forward_match = re.compile(r'forward (\d+)')
    down_match = re.compile(r'down (\d+)')
    up_match = re.compile(r'up (\d+)')

    def __init__(self, file_name):
        self._input: List[str] = Input(file_name).lines()

    def part1(self):
        depth = horizontal = 0

        for line in self._input:
            if match := self.forward_match.match(line):
                horizontal += int(match.group(1))
            elif match := self.down_match.match(line):
                depth += int(match.group(1))
            elif match := self.up_match.match(line):
                depth -= int(match.group(1))

        result = depth * horizontal

        print("Part 1:", result)

    def part2(self):
        depth = horizontal = aim = 0

        for line in self._input:
            if match := self.forward_match.match(line):
                x = int(match.group(1))
                horizontal += x
                depth += (aim * x)
            elif match := self.down_match.match(line):
                aim += int(match.group(1))
            elif match := self.up_match.match(line):
                aim -= int(match.group(1))
        result = depth * horizontal

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2021D2("2021/2.txt")
    code.part1()
    code.part2()
