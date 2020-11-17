from aoc.util.intcode import Intcode


class Y2019D21(object):
    def __init__(self, file_name):
        self.computer = Intcode(file_name)

    def part1(self):
        result = self._run(
            "NOT A J\n"
            "NOT B T\n"
            "OR T J\n"
            "NOT C T\n"
            "OR T J\n"
            "AND D J\n"
            "WALK\n"
        )

        print("Part 1:", result)

    def part2(self):
        result = self._run(
            "NOT H T\n"
            "OR C T\n"
            "AND B T\n"
            "AND A T\n"
            "NOT T J\n"
            "AND D J\n"
            "RUN\n"
        )

        print("Part 2:", result)

    def _run(self, *program: str):
        self.computer.reset()
        self.computer.run()
        self.computer.output_str()
        for command in program:
            self.computer.input_str(command)

        result = self.computer.output_str()

        if "Didn't make it across" in result:
            print(result)
            return -1
        else:
            return self.computer.output()


if __name__ == '__main__':
    code = Y2019D21("2019/21.txt")
    code.part1()
    code.part2()
