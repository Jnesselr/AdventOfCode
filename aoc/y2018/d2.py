from collections import Counter

from aoc.util.inputs import Input


class Y2018D2(object):
    def __init__(self, file_name):
        self.lines = Input(file_name).lines()

    def part1(self):
        count_3 = 0
        count_2 = 0

        for line in self.lines:
            counted_set = set(dict(Counter(line).most_common()).values())

            if 3 in counted_set:
                count_3 += 1
            if 2 in counted_set:
                count_2 += 1

        result = count_3 * count_2

        print("Part 1:", result)

    def part2(self):
        lines = sorted(self.lines)

        result = ""

        for index in range(len(lines)-1):
            a = lines[index]
            b = lines[index+1]
            diff_count = sum(1 for x, y in zip(a, b) if x != y)
            if diff_count == 1:
                result = "".join(x for x, y in zip(a, b) if x == y)
                break

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2018D2("2018/2.txt")
    code.part1()
    code.part2()
