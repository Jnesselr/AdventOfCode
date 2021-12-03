from typing import List, Callable

from aoc.util.inputs import Input


class Y2021D3(object):
    def __init__(self, file_name):
        self._input: List[str] = Input(file_name).lines()

    def part1(self):
        counter: List[int] = [0] * len(self._input[0])

        for line in self._input:
            for index, element in enumerate(line):
                if element == "1":
                    counter[index] += 1

        half = len(self._input) // 2
        gamma = int("".join("1" if x > half else "0" for x in counter), 2)
        epsilon = int(pow(2, len(counter))) - 1 - gamma

        result = gamma * epsilon

        print("Part 1:", result)

    def part2(self):
        oxygen_generator = self._get_filtered_value(self._input, lambda n0, n1: "1" if n1 >= n0 else "0")
        co2_scrubbing = self._get_filtered_value(self._input, lambda n0, n1: "0" if n1 >= n0 else "1")

        result = int(oxygen_generator, 2) * int(co2_scrubbing, 2)

        print("Part 2:", result)

    def _get_filtered_value(self, _in: List[str], func: Callable[[int, int], str]) -> str:
        num_zeros = len([x for x in _in if x[0] == "0"])
        num_ones = len(_in) - num_zeros
        search = func(num_zeros, num_ones)
        filtered_list = [x[1:] for x in _in if x[0] == search]

        if len(filtered_list) == 1:
            return search + filtered_list[0]
        else:
            return search + self._get_filtered_value(filtered_list, func)


if __name__ == '__main__':
    code = Y2021D3("2021/3.txt")
    code.part1()
    code.part2()
