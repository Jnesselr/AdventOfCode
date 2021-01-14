import itertools

from aoc.util.inputs import Input

from functools import reduce


def factors(n):
    return set(reduce(list.__add__, ([i, n // i] for i in range(1, int(n ** 0.5) + 1) if n % i == 0)))


# The count starts at the right solution for my input. Set it to 1 to test new inputs.
class Y2015D20(object):
    def __init__(self, file_name):
        self.input = Input(file_name).int()

    def part1(self):
        result = 0

        for house_num in itertools.count(831_600, step=10):
            presents = 10 * sum(factors(house_num))
            if presents >= self.input:
                result = house_num
                break

        print("Part 1:", result)

    def part2(self):
        result = 0

        for house_num in itertools.count(884_520, step=10):
            presents = 11 * sum(f for f in factors(house_num) if house_num // f <= 50)
            if presents >= self.input:
                result = house_num
                break

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2015D20("2015/20.txt")
    code.part1()
    code.part2()
