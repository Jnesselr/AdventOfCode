import re
from typing import List

from aoc.util.grid import Grid
from aoc.util.inputs import Input


class Computer:
    add_regex = re.compile(r'addx (-?\d+)')

    def __init__(self, lines: List[str]):
        self._lines = lines
        self.cycle = 0
        self.x = 1
        self.signal_sum = 0
        self.grid = Grid[str](40, 6)

    def run(self):
        for line in self._lines:
            if line == "noop":
                self.cycle += 1
                self._check_cycle()
            elif match := self.add_regex.match(line):
                self.cycle += 1
                self._check_cycle()
                self.cycle += 1
                self._check_cycle()
                self.x += int(match.group(1))

    def _check_cycle(self):
        if self.cycle == 20 or (self.cycle - 20) % 40 == 0:
            self.signal_sum = self.signal_sum + (self.cycle * self.x)

        col = self.cycle % 40 - 1
        row = (self.cycle - 1) // 40
        left_sprite = self.x - 1
        right_sprite = self.x + 1
        if left_sprite <= col <= right_sprite:
            self.grid[col, row] = '#'


class Y2022D10(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()

        self.computer = Computer(lines)
        self.computer.run()

    def part1(self):
        result = self.computer.signal_sum

        print("Part 1:", result)

    def part2(self):
        print("Part 2:")
        self.computer.grid.print()


if __name__ == '__main__':
    code = Y2022D10("2022/10.txt")
    code.part1()
    code.part2()
