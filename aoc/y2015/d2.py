from aoc.util.inputs import Input


class Y2015D2(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()

        self.presents = []
        for line in lines:
            self.presents.append(sorted([int(x) for x in line.split('x')]))

    def part1(self):
        result = 0

        for present in self.presents:
            l, w, h = present
            result += 2 * l * w + 2 * w * h + 2 * h * l + l * w

        print("Part 1:", result)

    def part2(self):
        result = 0

        for present in self.presents:
            l, w, h = present
            result += 2 * l + 2 * w + l * w * h

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2015D2("2015/2.txt")
    code.part1()
    code.part2()
