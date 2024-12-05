from collections import defaultdict
from functools import cmp_to_key

from aoc.util.inputs import Input


class Y2024D5(object):
    def __init__(self, file_name):
        groups = Input(file_name).grouped()
        self._dependencies: defaultdict[int, set[int]] = defaultdict(lambda: set())
        for line in groups[0]:
            a, b = line.split('|')
            self._dependencies[int(a)].add(int(b))  # a must be printed before b

        self._correct_update_count = 0
        self._incorrect_update_count = 0
        for line in groups[1]:
            update = [int(x) for x in line.split(',')]
            fixed_update = sorted(update, key=cmp_to_key(self._compare_pages))

            # If it was already correct, it'll be the same middle number
            middle_number = fixed_update[len(fixed_update) // 2]

            if update == fixed_update:
                self._correct_update_count += middle_number
            else:
                self._incorrect_update_count += middle_number

    def _compare_pages(self, page_a: int, page_b: int) -> int:
        if page_b in self._dependencies[page_a]:
            return -1  # page_a must be printed first
        if page_a in self._dependencies[page_b]:
            return 1  # page_b must be printed first
        return 0  # We can't tell these dependencies apart. We didn't see this for our data, but it's good to be thorough

    def part1(self):
        result = self._correct_update_count

        print("Part 1:", result)

    def part2(self):
        result = self._incorrect_update_count

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2024D5("2024/5.txt")
    code.part1()
    code.part2()
