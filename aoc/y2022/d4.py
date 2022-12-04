import re
from dataclasses import dataclass
from typing import List

from aoc.util.inputs import Input


@dataclass
class Pair:
    first_start: int
    first_end: int
    second_start: int
    second_end: int

    @property
    def fully_contains(self):
        first_contains_second = self.second_start >= self.first_start and self.second_end <= self.first_end
        second_contains_first = self.first_start >= self.second_start and self.first_end <= self.second_end
        return first_contains_second or second_contains_first

    @property
    def overlaps(self):
        first_overlaps_second = self.first_start <= self.second_start <= self.first_end
        second_overlaps_first = self.second_start <= self.first_start <= self.second_end
        return first_overlaps_second or second_overlaps_first


class Y2022D4(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()

        regex = re.compile(r'(\d+)-(\d+),(\d+)-(\d+)')
        self._pairs: List[Pair] = []
        for line in lines:
            match = regex.match(line)
            self._pairs.append(Pair(
                first_start=int(match.group(1)),
                first_end=int(match.group(2)),
                second_start=int(match.group(3)),
                second_end=int(match.group(4)),
            ))

    def part1(self):
        result = sum([1 for x in self._pairs if x.fully_contains])

        print("Part 1:", result)

    def part2(self):
        result = sum([1 for x in self._pairs if x.overlaps])

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2022D4("2022/4.txt")
    code.part1()
    code.part2()
