import math
import re
from dataclasses import dataclass
from typing import Optional

from aoc.util.inputs import Input


@dataclass(frozen=True)
class ClawMachine:
    a_button_x_change: int
    a_button_y_change: int
    b_button_x_change: int
    b_button_y_change: int
    prize_x: int
    prize_y: int

    @property
    def more_suffering(self) -> 'ClawMachine':
        inc = 10000000000000
        return ClawMachine(
            a_button_x_change=self.a_button_x_change,
            a_button_y_change=self.a_button_y_change,
            b_button_x_change=self.b_button_x_change,
            b_button_y_change=self.b_button_y_change,
            prize_x=self.prize_x + inc,
            prize_y=self.prize_y + inc,
        )

    @property
    def presses_to_prize(self) -> Optional[int]:
        a_lcm = math.lcm(self.a_button_x_change, self.a_button_y_change)
        ax_div = a_lcm // self.a_button_x_change
        ay_div = -a_lcm // self.a_button_y_change

        # self.a_button_x_change * ax_div + self.a_button_y_change * ay_div == 0
        b_sum = self.b_button_x_change * ax_div + self.b_button_y_change * ay_div
        prize_sum = self.prize_x * ax_div + self.prize_y * ay_div

        if b_sum * prize_sum < 0:  # Is only one of their signs negative?
            return None

        b_presses = prize_sum / b_sum
        if round(b_presses) != b_presses:
            return None  # Not an integer solution

        # Now we just have to use one of the other equations to calculate a presses
        a_presses = (self.prize_x - (b_presses * self.b_button_x_change)) / self.a_button_x_change
        if round(a_presses) != a_presses:
            return None  # Not an integer solution

        return round(a_presses) * 3 + round(b_presses) * 1


class Y2024D13(object):
    button_a_re = re.compile(r'Button A: X\+(\d+), Y\+(\d+)')
    button_b_re = re.compile(r'Button B: X\+(\d+), Y\+(\d+)')
    prize_re = re.compile(r'Prize: X=(\d+), Y=(\d+)')

    def __init__(self, file_name):
        groups = Input(file_name).grouped()
        self._machines: list[ClawMachine] = []
        for group in groups:
            a_button_x_change: int = 0
            a_button_y_change: int = 0
            b_button_x_change: int = 0
            b_button_y_change: int = 0
            prize_x: int = 0
            prize_y: int = 0
            for line in group:
                if (match := self.button_a_re.match(line)) is not None:
                    a_button_x_change = int(match.group(1))
                    a_button_y_change = int(match.group(2))
                elif (match := self.button_b_re.match(line)) is not None:
                    b_button_x_change = int(match.group(1))
                    b_button_y_change = int(match.group(2))
                elif (match := self.prize_re.match(line)) is not None:
                    prize_x = int(match.group(1))
                    prize_y = int(match.group(2))
                else:
                    raise Exception(f"Could not match line: {line}")

            self._machines.append(ClawMachine(
                a_button_x_change=a_button_x_change,
                a_button_y_change=a_button_y_change,
                b_button_x_change=b_button_x_change,
                b_button_y_change=b_button_y_change,
                prize_x=prize_x,
                prize_y=prize_y,
            ))

    def part1(self):
        result = 0

        for machine in self._machines:
            presses = machine.presses_to_prize
            if presses is not None:
                result += presses

        print("Part 1:", result)

    def part2(self):
        result = 0

        for machine in self._machines:
            presses = machine.more_suffering.presses_to_prize
            if presses is not None:
                result += presses

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2024D13("2024/13.txt")
    code.part1()
    code.part2()
