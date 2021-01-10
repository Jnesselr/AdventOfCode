from aoc.util.inputs import Input


class Y2016D20(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.pairs = []

        for line in lines:
            start, end = line.split('-')
            self.pairs.append((int(start), int(end)))

        max_value = 4294967295 + 1
        self.pairs.append((max_value, max_value))

        self.pairs = sorted(self.pairs)

    def part1(self):
        result = 0

        for pair in self.pairs:
            start, end = pair
            if result > end:
                continue
            if start > result:
                break

            result = end + 1

        print("Part 1:", result)

    def part2(self):
        result = 0
        current = 0

        for pair in self.pairs:
            start, end = pair
            if current > end:
                continue
            if start > current:
                result += start - current

            current = end + 1

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2016D20("2016/20.txt")
    code.part1()
    code.part2()
