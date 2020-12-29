from collections import Counter

from aoc.util.inputs import Input


class Y2016D6(object):
    def __init__(self, file_name):
        self.lines = Input(file_name).lines()

        self.most_common = ""
        self.least_common = ""

        by_index = {}

        for line in self.lines:
            for index, character in enumerate(line):
                by_index.setdefault(index, []).append(character)

        for key, values in by_index.items():
            common = list(Counter(values).most_common())

            most_common_character = sorted(common, key=lambda x: -x[1])[0][0]
            self.most_common += most_common_character

            least_common_character = sorted(common, key=lambda x: x[1])[0][0]
            self.least_common += least_common_character

    def part1(self):
        result = self.most_common

        print("Part 1:", result)

    def part2(self):
        result = self.least_common

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2016D6("2016/6.txt")
    code.part1()
    code.part2()
