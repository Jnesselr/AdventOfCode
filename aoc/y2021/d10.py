from typing import List

from aoc.util.inputs import Input


class Y2021D10(object):
    _bad_close_points = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }
    _closing = {
        '(': ')',
        '[': ']',
        '{': '}',
        '<': '>',
    }
    _good_close_points = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4,
    }

    def __init__(self, file_name):
        self._lines = Input(file_name).lines()
        self._bad_close_points_total = 0

        incomplete_points_list = []
        for line in self._lines:
            incomplete_points_line = 0
            stack: List[str] = []
            while len(line) > 0:
                first = line[0]
                line = line[1:]
                if first in ')]}>':
                    if len(stack) == 0:
                        self._bad_close_points_total += self._bad_close_points[first]
                        line = ""
                        stack = []
                        break

                    popped = stack.pop()
                    if popped == '(' and first == ')':
                        continue
                    elif popped == '[' and first == ']':
                        continue
                    elif popped == '{' and first == '}':
                        continue
                    elif popped == '<' and first == '>':
                        continue
                    else:
                        self._bad_close_points_total += self._bad_close_points[first]
                        line = ""
                        stack = []
                        break
                else:
                    stack.append(first)

            if len(stack) > 0:
                while len(stack) > 0:
                    popped = stack.pop()
                    closing = self._closing[popped]
                    incomplete_points_line = incomplete_points_line * 5 + self._good_close_points[closing]
                incomplete_points_list.append(incomplete_points_line)

        self._incomplete_points_total = sorted(incomplete_points_list)[len(incomplete_points_list) // 2]

    def part1(self):
        print("Part 1:", self._bad_close_points_total)

    def part2(self):
        print("Part 2:", self._incomplete_points_total)


if __name__ == '__main__':
    code = Y2021D10("2021/10.txt")
    code.part1()
    code.part2()
