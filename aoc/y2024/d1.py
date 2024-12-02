from collections import Counter

from aoc.util.inputs import Input


class Y2024D1(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self._left_location_ids: list[int] = []
        self._right_location_ids: list[int] = []

        for line in lines:
            while "  " in line:
                line = line.replace("  ", " ")

            a, b = line.split(" ")
            self._left_location_ids.append(int(a))
            self._right_location_ids.append(int(b))

    def part1(self):
        left_copy = list(self._left_location_ids)
        right_copy = list(self._right_location_ids)

        result = 0

        while len(left_copy) > 0:
            left = min(left_copy)
            right = min(right_copy)

            result += abs(right - left)

            left_copy.remove(left)
            right_copy.remove(right)

        print("Part 1:", result)

    def part2(self):
        c = Counter(self._right_location_ids)

        result = 0

        for left in self._left_location_ids:
            result += left * c[left]

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2024D1("2024/1.txt")
    code.part1()
    code.part2()
