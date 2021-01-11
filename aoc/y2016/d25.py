from aoc.util.inputs import Input
from aoc.y2016.assembunny import Assembunny


class Y2016D25(object):
    def __init__(self, file_name):
        self.assembunny = Assembunny(Input(file_name).lines())

    def part1(self):
        # Found via reverse engineering. Basically, what number + 2550 was alternating 1s and 0s in binary.
        result = 180

        self.assembunny.registers[0] = result
        # Only run if you want to prove it produces the correct signal
        # self.assembunny.run()

        print("Part 1:", result)

    @staticmethod
    def part2():
        pass


if __name__ == '__main__':
    code = Y2016D25("2016/25.txt")
    code.part1()
    code.part2()
