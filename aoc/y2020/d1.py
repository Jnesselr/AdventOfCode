from aoc.util.inputs import Input


class Y2020D1(object):
    def __init__(self, file_name):
        self.input = [int(x) for x in Input(file_name).lines()]

    def part1(self):
        result = 0
        for x in self.input:
            for y in self.input:
                if x+y == 2020:
                    result = x*y

        print("Part 1:", result)

    def part2(self):
        result = 0

        for x in self.input:
            for y in self.input:
                if x+y > 2020:
                    continue
                for z in self.input:
                    if x+y+z == 2020:
                        result = x*y*z

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2020D1("2020/1.txt")
    code.part1()
    code.part2()
