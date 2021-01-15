import re

from aoc.util.inputs import Input


class Y2015D25(object):
    def __init__(self, file_name):
        line = Input(file_name).line()

        self.row = int(re.search(r'row (\d+)', line).group(1))
        self.column = int(re.search(r'column (\d+)', line).group(1))

    def part1(self):
        power = sum(range((self.row + self.column - 1))) + self.column - 1
        mod = 33554393
        result = (20151125 * pow(252533, power, mod)) % mod

        print("Part 1:", result)

    def part2(self):
        pass


if __name__ == '__main__':
    code = Y2015D25("2015/25.txt")
    code.part1()
    code.part2()
