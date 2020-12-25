from aoc.util.inputs import Input


class Y2020D25(object):
    magic = 20201227

    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.pub1 = int(lines[0])
        self.pub2 = int(lines[1])

    def part1(self):
        result = 0
        value = 1
        loop_count = 0
        while result == 0:
            loop_count += 1
            value = (value * 7) % self.magic

            if value == self.pub1:
                result = pow(self.pub2, loop_count, self.magic)
            if value == self.pub2:
                result = pow(self.pub1, loop_count, self.magic)

        print("Part 1:", result)

    def part2(self):
        pass


if __name__ == '__main__':
    code = Y2020D25("2020/25.txt")
    code.part1()
    code.part2()
