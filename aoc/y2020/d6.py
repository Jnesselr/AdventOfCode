from aoc.util import alphabet
from aoc.util.inputs import Input


class Y2020D6(object):
    def __init__(self, file_name):
        self.groups = [[set(person) for person in group] for group in Input(file_name).grouped()]

    def part1(self):
        result = 0

        for group in self.groups:
            all_set = set()
            for person in group:
                all_set = all_set.union(person)

            result += len(all_set)

        print("Part 1:", result)

    def part2(self):
        result = 0

        for group in self.groups:
            all_set = set(alphabet)
            for person in group:
                all_set = all_set.intersection(person)

            result += len(all_set)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2020D6("2020/6.txt")
    code.part1()
    code.part2()
