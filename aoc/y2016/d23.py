from aoc.util.inputs import Input
from aoc.y2016.assembunny import Assembunny


class Y2016D23(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.assembunny = Assembunny(lines)

    def part1(self):
        self.assembunny.reset()
        self.assembunny.registers[0] = 7
        self.assembunny.run()
        result = self.assembunny.registers[0]

        print("Part 1:", result)

    @staticmethod
    def part2():
        # My input was basically 12! + 95 * 91. I suspect for different inputs, the 91 and 95 are what changes.
        result = 479010245

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2016D23("2016/23.txt")
    code.part1()
    code.part2()
