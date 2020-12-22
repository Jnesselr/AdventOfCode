from aoc.util.inputs import Input
from aoc.y2018.watch import WatchVM, Igtrr, Idvup


class Y2018D19(object):
    def __init__(self, file_name):
        self.vm = WatchVM(Input(file_name).lines())

        # Some modifications to make this vm finish this century for part 1
        self.vm.instructions[8] = Idvup(2, 3, 5)  # Yes, custom instruction
        gtrr = self.vm.instructions[9]
        self.vm.instructions[9] = Igtrr(5, gtrr.b, gtrr.c)

    def part1(self):
        self.vm.reset()
        self.vm.run()
        result = self.vm.registers[0]

        print("Part 1:", result)

    @staticmethod
    def part2():
        # This code is _very_ tied to my input, but this whole day is so... yeah.
        # The code tries to find all factors of this number and sum them up. It does this one number at a time.
        # Very. Inefficiently.

        number = 10551403
        result = sum(x for x in range(1, number + 1) if number % x == 0)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2018D19("2018/19.txt")
    code.part1()
    code.part2()
