import itertools

from aoc.util.inputs import Input


class Y2017D2(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.rows = []

        for line in lines:
            self.rows.append([int(x) for x in line.split('\t')])

    def part1(self):
        result = sum(max(row) - min(row) for row in self.rows)

        print("Part 1:", result)

    def part2(self):
        result = sum([x // y for x, y in itertools.product(row, row) if x != y and x % y == 0][0] for row in self.rows)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2017D2("2017/2.txt")
    code.part1()
    code.part2()
