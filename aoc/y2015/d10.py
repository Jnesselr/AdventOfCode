import itertools

from aoc.util.inputs import Input


class Y2015D11(object):
    def __init__(self, file_name):
        sequence = Input(file_name).line()

        self.length_at_40 = 0
        self.length_at_50 = 0

        for iteration in range(50):
            new_sequence = ""
            index = 0

            while index < len(sequence):
                value = sequence[index]
                for i in itertools.count(1):
                    index += 1
                    if index >= len(sequence) or sequence[index] != value:
                        new_sequence += str(i) + str(value)
                        break

            sequence = new_sequence

            if iteration == 39:
                self.length_at_40 = len(sequence)
            if iteration == 49:
                self.length_at_50 = len(sequence)

    def part1(self):
        result = self.length_at_40

        print("Part 1:", result)

    def part2(self):
        result = self.length_at_50

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2015D11("2015/10.txt")
    code.part1()
    code.part2()
