from aoc.util.inputs import Input


class Y2022D1(object):
    def __init__(self, file_name):
        _grouped = Input(file_name).grouped()
        self._snacks_per = [sum([int(y) for y in x]) for x in _grouped]

    def part1(self):
        result = max(self._snacks_per)

        print("Part 1:", result)

    def part2(self):
        s = sorted(self._snacks_per)
        result = sum(s[-3:])

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2022D1("2022/1.txt")
    code.part1()
    code.part2()
