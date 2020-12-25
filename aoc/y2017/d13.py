import itertools
from typing import Dict

from aoc.util.inputs import Input


class Y2017D13(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()

        self.firewall: Dict[int, int] = {}

        for line in lines:
            key, value = line.split(': ')
            self.firewall[int(key)] = int(value)

    def part1(self):
        result = 0

        for _depth, _range in self.firewall.items():
            if _depth % ((_range - 1) * 2) == 0:
                result += _depth * _range

        print("Part 1:", result)

    def part2(self):
        result = 0

        for delay in itertools.count():
            caught = False
            for _depth, _range in self.firewall.items():
                if (_depth + delay) % ((_range - 1) * 2) == 0:
                    caught = True
                    break
            if not caught:
                result = delay
                break

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2017D13("2017/13.txt")
    code.part1()
    code.part2()
