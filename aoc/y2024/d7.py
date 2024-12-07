import operator
from dataclasses import dataclass
from itertools import product

from tqdm import tqdm

from aoc.util.inputs import Input


@dataclass
class Calibration:
    result: int
    values: list[int]


class Y2024D7(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()

        self._calibrations: list[Calibration] = []
        for line in lines:
            result, numbers = line.split(':')

            self._calibrations.append(Calibration(
                result=int(result.strip()),
                values=[int(x) for x in numbers.strip().split()]
            ))

    def part1(self):
        result = 0

        for calibration in self._calibrations:
            if self._is_valid_result(calibration):
                result += calibration.result

        print("Part 1:", result)

    def part2(self):
        result = 0

        for calibration in self._calibrations:
            if self._is_valid_result(calibration, True):
                result += calibration.result

        print("Part 2:", result)

    @staticmethod
    def _is_valid_result(calibration: Calibration, support_concat=False) -> bool:
        valid_operators = [operator.add, operator.mul]

        if support_concat:
            def _concat(a: int, b: int) -> int:
                return int(str(a) + str(b))

            valid_operators.append(_concat)

        for ops in product(valid_operators, repeat=len(calibration.values) - 1):
            values = calibration.values
            while len(ops) > 0:
                new_value = ops[0](values[0], values[1])
                values = [new_value] + values[2:]
                ops = ops[1:]

            if values[0] == calibration.result:
                return True

        return False


if __name__ == '__main__':
    code = Y2024D7("2024/7.txt")
    code.part1()
    code.part2()
