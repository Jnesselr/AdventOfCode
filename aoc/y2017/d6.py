from typing import Set, Dict

from aoc.util.inputs import Input


class Y2017D6(object):
    def __init__(self, file_name):
        banks = [int(x) for x in Input(file_name).line().split('\t')]

        self.redistribution_cycles = 0
        seen: Dict[str, int] = {}
        num_banks = len(banks)
        while True:
            bank_str = ",".join(str(x) for x in banks)

            if bank_str in seen:
                break
            seen[bank_str] = self.redistribution_cycles

            index, value = max(enumerate(banks), key=lambda x: (x[1], -x[0]))
            banks[index] = 0
            value_to_fill = ((value - 1) // num_banks) + 1
            num_to_fill = value // value_to_fill
            for i in range(num_to_fill):
                banks[(index + i + 1) % num_banks] += value_to_fill

            banks[(index + num_to_fill + 1) % num_banks] += value - (value_to_fill * num_to_fill)

            self.redistribution_cycles += 1

        self.cycle_size = self.redistribution_cycles - seen[bank_str]

    def part1(self):
        result = self.redistribution_cycles

        print("Part 1:", result)

    def part2(self):
        result = self.cycle_size

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2017D6("2017/6.txt")
    code.part1()
    code.part2()
