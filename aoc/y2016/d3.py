import re
from dataclasses import dataclass
from typing import List

from aoc.util.inputs import Input


@dataclass(frozen=True)
class Triangle(object):
    side_a: int
    side_b: int
    side_c: int

    @property
    def valid(self) -> bool:
        if self.side_a + self.side_b <= self.side_c:
            return False
        if self.side_b + self.side_c <= self.side_a:
            return False
        if self.side_c + self.side_a <= self.side_b:
            return False
        return True


class Y2016D3(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.triangle_rows: List[Triangle] = []
        self.triangle_cols: List[Triangle] = []

        running_triangles = {}
        for line in lines:
            matched = re.match(r'\s*(\d+)\s+(\d+)\s+(\d+)', line)
            a = int(matched.group(1))
            b = int(matched.group(2))
            c = int(matched.group(3))
            self.triangle_rows.append(Triangle(side_a=a, side_b=b, side_c=c))

            running_triangles.setdefault(1, []).append(a)
            running_triangles.setdefault(2, []).append(b)
            running_triangles.setdefault(3, []).append(c)

            if len(running_triangles[1]) == 3:
                for value in running_triangles.values():
                    self.triangle_cols.append(Triangle(value[0], value[1], value[2]))
                running_triangles = {}


    def part1(self):
        result = sum(1 for triangle in self.triangle_rows if triangle.valid)

        print("Part 1:", result)

    def part2(self):
        result = sum(1 for triangle in self.triangle_cols if triangle.valid)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2016D3("2016/3.txt")
    code.part1()
    code.part2()
