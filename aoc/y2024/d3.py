import re

from aoc.util.inputs import Input


class Y2024D3(object):
    multiply_regex = re.compile(r'mul\(([0-9]{1,3}),([0-9]{1,3})\)')
    do_regex = re.compile(r'do\(\)')
    dont_regex = re.compile(r'don\'t\(\)')

    def __init__(self, file_name):
        self._lines = Input(file_name).lines()

    def part1(self):
        result = 0

        for line in self._lines:
            search = self.multiply_regex.findall(line)
            for a, b in search:
                result += int(a) * int(b)

        print("Part 1:", result)

    def part2(self):
        result = 0

        do_enabled = True
        for line in self._lines:
            position = 0
            while True:
                multiply_match = self.multiply_regex.search(line, position)
                do_match = self.do_regex.search(line, position)
                dont_match = self.dont_regex.search(line, position)

                if multiply_match is None and do_match is None and dont_match is None:
                    break

                multiply_start = multiply_match.span()[0] if multiply_match is not None else len(line)
                do_start = do_match.span()[0] if do_match is not None else len(line)
                dont_start = dont_match.span()[0] if dont_match is not None else len(line)

                if do_start < multiply_start and do_start < dont_start:
                    do_enabled = True
                    position = do_match.span()[-1]
                elif dont_start < multiply_start and dont_start < do_start:
                    do_enabled = False
                    position = dont_match.span()[-1]
                else:
                    if do_enabled:
                        result += int(multiply_match.group(1)) * int(multiply_match.group(2))
                    position = multiply_match.span()[-1]

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2024D3("2024/3.txt")
    code.part1()
    code.part2()
