from typing import Dict

from aoc.util.inputs import Input


def to_snafu(number: int) -> str:
    result = ""

    # Start by getting the bounds that can capture it
    place_value = 0
    max_negative = 1
    max_positive = 2
    while True:
        if max_negative <= number <= max_positive:
            break
        place_value += 1
        max_negative = max_negative * 5 + -2
        max_positive = max_positive * 5 + 2

    while place_value > -1:
        int_power = int(pow(5, place_value))
        options: Dict[str, int] = {
            "=": -2 * int_power,
            "-": -1 * int_power,
            "0": 0,
            "1": 1 * int_power,
            "2": 2 * int_power,
        }

        min_c2z = 5 * int_power
        min_value = 5 * int_power
        min_item = None

        for item, value in options.items():
            close_to_zero_value = number - value
            # print(place_value, number, item, value, close_to_zero_value)
            if abs(close_to_zero_value) < abs(min_c2z):
                min_c2z = close_to_zero_value
                min_value = value
                min_item = item

        # print()
        result += min_item
        number -= min_value
        place_value -= 1

    return result


def from_snafu(snafu: str) -> int:
    result = 0
    place_value = 1

    for letter in snafu[::-1]:
        if letter == '2':
            result += 2 * place_value
        elif letter == '1':
            result += place_value
        elif letter == '0':
            pass
        elif letter == '-':
            result += -1 * place_value
        elif letter == '=':
            result += -2 * place_value

        place_value *= 5

    return result


class Y2022D25(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.sum = 0
        for line in lines:
            self.sum += from_snafu(line)

    def part1(self):
        result = to_snafu(self.sum)

        print("Part 1:", result)

    def part2(self):
        result = 0

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2022D25("2022/25.txt")
    code.part1()
    code.part2()
