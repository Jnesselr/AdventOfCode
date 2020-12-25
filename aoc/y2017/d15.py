import re

from aoc.util.inputs import Input


class Y2017D15(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()

        self.start_a = None
        self.start_b = None

        for line in lines:
            matched = re.match(r'Generator (\w) starts with (\d+)', line)
            if matched.group(1) == 'A':
                self.start_a = int(matched.group(2))
            elif matched.group(1) == 'B':
                self.start_b = int(matched.group(2))

    def part1(self):
        result = 0

        generator_a = self._generator(self.start_a, 16807)
        generator_b = self._generator(self.start_b, 48271)

        for _ in range(40000000):
            a_value = next(generator_a) & 0xffff
            b_value = next(generator_b) & 0xffff

            if a_value == b_value:
                result += 1

        print("Part 1:", result)

    def part2(self):
        result = 0

        generator_a = self._generator(self.start_a, 16807, 4)
        generator_b = self._generator(self.start_b, 48271, 8)

        for _ in range(5000000):
            a_value = next(generator_a) & 0xffff
            b_value = next(generator_b) & 0xffff

            if a_value == b_value:
                result += 1

        print("Part 2:", result)

    @staticmethod
    def _generator(start, factor, consider_multiples_of=1):
        value = start
        while True:
            value = (value * factor) % 2147483647
            if value % consider_multiples_of == 0:
                yield value


if __name__ == '__main__':
    code = Y2017D15("2017/15.txt")
    code.part1()
    code.part2()
