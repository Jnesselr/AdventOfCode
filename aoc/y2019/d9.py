from aoc.util.inputs import Input
from aoc.util.intcode import Intcode


class Y2019D9(object):
    def __init__(self, file_name):
        self.computer = Intcode(file_name)

    def part1(self):
        self.computer.reset()
        self.computer.run()
        self.computer.input(1)

        outputs = []
        while not self.computer.halted:
            outputs.append(self.computer.output())

        if len(outputs) == 1:
            print("Part 1:", outputs[-1])
        else:
            print("Something went wrong, invalid output:")
            for output in outputs:
                print(output)

    def part2(self):
        self.computer.reset()
        self.computer.run()
        self.computer.input(2)

        print("Part 2:", self.computer.output())


if __name__ == '__main__':
    code = Y2019D9("2019/9.txt")
    code.part1()
    code.part2()
