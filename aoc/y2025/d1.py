from aoc.util.inputs import Input


class Dial:
    def __init__(self):
        self._position = 50
        self._exactly_zero_counter = 0
        self._touches_zero_counter = 0

    def turn(self, line: str) -> None:
        amount = int(line[1:])
        delta = 1 if line[0] == 'R' else -1

        for i in range(amount):
            self._position += delta
            if self._position < 0:
                self._position += 100

            if self._position >= 100:
                self._position = 0

            if self._position == 0:
                self._touches_zero_counter += 1

        if self._position == 0:
            self._exactly_zero_counter += 1

    @property
    def exactly_zero_counter(self) -> int:
        return self._exactly_zero_counter

    @property
    def touches_zero_counter(self) -> int:
        return self._touches_zero_counter


class Y2025D1(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self._dial = Dial()

        for line in lines:
            self._dial.turn(line)

    def part1(self):
        result = self._dial.exactly_zero_counter

        print("Part 1:", result)

    def part2(self):
        result = self._dial.touches_zero_counter

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2025D1("2025/1.txt")
    code.part1()
    code.part2()
