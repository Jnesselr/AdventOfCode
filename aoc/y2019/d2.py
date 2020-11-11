from aoc.util.inputs import Input
from aoc.util.intcode import Intcode


class Y2019D2(object):
    def __init__(self, file_name):
        self.computer = Intcode(file_name)

    def part1(self):
        self.computer.reset()
        self.computer.ram[1] = 12
        self.computer.ram[2] = 2
        self.computer.run()

        print("Part 1:", self.computer.ram[0])

    def part2(self):
        result = 0
        for noun in range(100):
            for verb in range(100):
                self.computer.reset()
                self.computer.ram[1] = noun
                self.computer.ram[2] = verb
                self.computer.run()

                if self.computer.ram[0] == 19690720:
                    result = 100 * noun + verb
                    break

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2019D2("2019/2.txt")
    code.part1()
    code.part2()
