from typing import List, Dict

from aoc.util.inputs import Input


class Y2021D6(object):
    def __init__(self, file_name):
        line = Input(file_name).line()
        self._fish: List[int] = [int(x) for x in line.split(',')]

    def part1(self):
        result = self._count_fish_after_day(80)

        print("Part 1:", result)

    def part2(self):
        result = self._count_fish_after_day(256)

        print("Part 2:", result)

    def _count_fish_after_day(self, end_day: int) -> int:
        new_fish_after_day: Dict[int, int] = {}

        for fish_cycle in self._fish:
            fish_cycle += 1
            while fish_cycle <= end_day:
                new_fish_after_day[fish_cycle] = new_fish_after_day.setdefault(fish_cycle, 0) + 1
                fish_cycle += 7

        for day in range(end_day + 1):
            new_fish_count = new_fish_after_day.setdefault(day, 0)
            fish_cycle = day + 8 + 1
            while fish_cycle <= end_day:
                new_fish_after_day[fish_cycle] = new_fish_after_day.setdefault(fish_cycle, 0) + new_fish_count
                fish_cycle += 7

        return sum(new_fish_after_day.values()) + len(self._fish)


if __name__ == '__main__':
    code = Y2021D6("2021/6.txt")
    code.part1()
    code.part2()
