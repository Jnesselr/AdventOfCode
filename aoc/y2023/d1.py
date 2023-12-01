from aoc.util.inputs import Input


class Y2023D1(object):
    def __init__(self, file_name):
        self.lines = Input(file_name).lines()

    def part1(self):
        result = 0

        for line in self.lines:
            digits = list(self._get_digits(line))
            result += int(digits[0]) * 10 + int(digits[-1])

        print("Part 1:", result)

    def part2(self):
        result = 0

        for line in self.lines:
            digits = list(self._get_digits(line, include_words=True))
            addition = int(digits[0]) * 10 + int(digits[-1])
            result += addition

        print("Part 2:", result)

    @staticmethod
    def _get_digits(line, include_words=False):
        m = {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
        }

        for i in range(len(line)):
            if line[i].isdigit():
                yield int(line[i])
            if include_words:
                for key in m.keys():
                    if line[i:].startswith(key):
                        yield m[key]


if __name__ == '__main__':
    code = Y2023D1("2023/1.txt")
    code.part1()
    code.part2()
