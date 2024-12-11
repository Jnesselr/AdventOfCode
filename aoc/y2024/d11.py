from dataclasses import dataclass
from typing import Tuple

from aoc.util.inputs import Input


@dataclass(frozen=True)
class SplitCache:
    in_value: int
    left_out_value: int
    right_out_value: int
    iterations_to_split: int


class StoneBlinker:
    def __init__(self, max_iterations: int):
        self._max_iterations: int = max_iterations
        self._split_cache: dict[int, SplitCache] = {}
        # key is (stone, iteration), value is how many this stone splits into after those iterations
        self._split_results: dict[Tuple[int, int], int] = {}

    def __call__(self, stone: int) -> int:
        return self._recurse(stone)

    @staticmethod
    def _get_cache_value(original_stone: int) -> SplitCache:
        stones = [original_stone]
        iteration = 0
        while len(stones) != 2:
            stone = stones[0]
            if stone == 0:
                stones = [1]
            elif len(stone_str := str(stone)) % 2 == 0:
                midpoint = len(stone_str) // 2
                stones = [int(stone_str[:midpoint]), int(stone_str[midpoint:])]
            else:
                stones = [stone * 2024]
            iteration += 1

        return SplitCache(
            in_value=original_stone,
            left_out_value=stones[0],
            right_out_value=stones[1],
            iterations_to_split=iteration
        )

    def _recurse(self, stone: int, iteration: int = 0) -> int:
        result_tuple = (stone, iteration)
        if result_tuple in self._split_results:
            return self._split_results[result_tuple]

        if stone not in self._split_cache:
            self._split_cache[stone] = self._get_cache_value(stone)

        cache: SplitCache = self._split_cache[stone]

        if iteration + cache.iterations_to_split > self._max_iterations:
            self._split_results[result_tuple] = 1  # We can only count ourselves
        else:
            self._split_results[result_tuple] = self._recurse(
                cache.left_out_value,
                iteration + cache.iterations_to_split
            ) + self._recurse(
                cache.right_out_value,
                iteration + cache.iterations_to_split
            )

        return self._split_results[result_tuple]


class Y2024D11(object):
    def __init__(self, file_name):
        self._stones: list[int] = Input(file_name).int_line()

    def part1(self):
        blinker = StoneBlinker(25)
        result = sum(blinker(x) for x in self._stones)

        print("Part 1:", result)

    def part2(self):
        blinker = StoneBlinker(75)
        result = sum(blinker(x) for x in self._stones)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2024D11("2024/11.txt")
    code.part1()
    code.part2()
