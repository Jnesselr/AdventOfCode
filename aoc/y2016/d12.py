from aoc.util.inputs import Input
from aoc.y2016.assembunny import Assembunny


class Y2016D12(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.computer = Assembunny(lines)

    def part1(self):
        self.computer.reset()
        self.computer.run()
        result = self.computer.registers[0]

        print("Part 1:", result)

    def part2(self):
        self.computer.reset()
        self.computer.registers[2] = 1
        self.computer.run()
        result = self.computer.registers[0]

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2016D12("2016/12.txt")
    code.part1()
    code.part2()
