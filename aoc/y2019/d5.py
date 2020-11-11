from aoc.util.intcode import Intcode


class Y2019D5(object):
    def __init__(self, file_name):
        self.computer = Intcode(file_name)

    def part1(self):
        self.computer.reset()
        self.computer.run()
        self.computer.input(1)

        outputs = []
        while not self.computer.halted:
            self.computer.run()

            if self.computer.has_output:
                output = self.computer.output()
                outputs.append(output)

        is_valid_output = len(list(filter(None, outputs))) == 1 and outputs[-1] > 0

        if is_valid_output:
            print("Part 1:", outputs[-1])
        else:
            print("INVALID!")
            for output in outputs:
                print(output)

    def part2(self):
        self.computer.reset()
        self.computer.run()
        self.computer.input(5)
        self.computer.run()
        result = self.computer.output()
        self.computer.run()

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2019D5("2019/5.txt")
    code.part1()
    code.part2()
