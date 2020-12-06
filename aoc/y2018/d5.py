from aoc.util import alphabet
from aoc.util.inputs import Input


class Y2018D5(object):
    def __init__(self, file_name):
        self.polymer = Input(file_name).line()

    def part1(self):
        polymer = self.polymer

        polymer = self._reduce_polymer(polymer)

        result = len(polymer)

        print("Part 1:", result)

    def part2(self):
        result = len(self.polymer)

        for letter in alphabet:
            polymer = self.polymer.replace(letter, '').replace(letter.upper(), '')
            polymer = self._reduce_polymer(polymer)
            result = min(result, len(polymer))

        print("Part 2:", result)

    @staticmethod
    def _reduce_polymer(polymer):
        index = 0
        while index < len(polymer) - 1:
            first = polymer[index]
            second = polymer[index + 1]

            matching = first.lower() == second.lower()
            different_case = (first.islower() and second.isupper()) or (first.isupper() and second.islower())

            if matching and different_case:
                polymer = polymer.replace(first + second, '')
                if index > 0:
                    index -= 1
            else:
                index += 1
        return polymer


if __name__ == '__main__':
    code = Y2018D5("2018/5.txt")
    code.part1()
    code.part2()
