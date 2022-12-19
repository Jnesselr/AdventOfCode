import enum
from collections import Counter
from dataclasses import dataclass
from itertools import product
from queue import Queue
from typing import List

from aoc.util.inputs import Input


class SideFacing(enum.Enum):
    XY = enum.auto()
    YZ = enum.auto()
    XZ = enum.auto()


@dataclass(frozen=True)
class Cube:
    x: int
    y: int
    z: int

    @property
    def adjacent(self) -> set['Cube']:
        result = set()
        result.add(Cube(self.x - 1, self.y, self.z))
        result.add(Cube(self.x + 1, self.y, self.z))
        result.add(Cube(self.x, self.y - 1, self.z))
        result.add(Cube(self.x, self.y + 1, self.z))
        result.add(Cube(self.x, self.y, self.z - 1))
        result.add(Cube(self.x, self.y, self.z + 1))
        return result


@dataclass
class Grouping:
    enclosed: bool
    cubes: set[Cube]


class Y2022D18(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.cubes: set[Cube] = set()

        self.min_x = 1e24
        self.max_x = -1e24
        self.min_y = 1e24
        self.max_y = -1e24
        self.min_z = 1e24
        self.max_z = -1e24

        for line in lines:
            x, y, z = line.split(',')
            cube = Cube(x=int(x), y=int(y), z=int(z))
            self.cubes.add(cube)

            self.min_x = min(self.min_x, cube.x)
            self.max_x = max(self.max_x, cube.x)
            self.min_y = min(self.min_y, cube.y)
            self.max_y = max(self.max_y, cube.y)
            self.min_z = min(self.min_z, cube.z)
            self.max_z = max(self.max_z, cube.z)

    @staticmethod
    def _get_exposed_sides(cubes: set[Cube]) -> int:
        all_sides = Counter()

        for cube in cubes:
            x, y, z = cube.x, cube.y, cube.z

            # A cube to side space so we can compare sides
            sides = [
                (x, y, z, SideFacing.YZ),
                (x + 1, y, z, SideFacing.YZ),
                (x, y, z, SideFacing.XZ),
                (x, y + 1, z, SideFacing.XZ),
                (x, y, z, SideFacing.XY),
                (x, y, z + 1, SideFacing.XY),
            ]
            for side in sides:
                all_sides[side] += 1

        exposed_sides = set(side for side, count in all_sides.items() if count == 1)
        return len(exposed_sides)

    def _get_groupings(self) -> List[Grouping]:
        groupings: List[Grouping] = []

        x_range = range(self.min_x, self.max_x + 1)
        y_range = range(self.min_y, self.max_y + 1)
        z_range = range(self.min_z, self.max_z + 1)
        all_cubes = set()
        for x, y, z in product(x_range, y_range, z_range):
            all_cubes.add(Cube(x, y, z))

        handled = set(self.cubes)
        for cube in all_cubes:
            if cube in handled:
                continue

            group = Grouping(
                enclosed=True,
                cubes={cube}
            )

            q = Queue()
            q.put(cube)
            handled.add(cube)

            while not q.empty():
                cube: Cube = q.get()
                for other_cube in cube.adjacent:
                    if other_cube.x < self.min_x or other_cube.x > self.max_x:
                        continue

                    if other_cube.y < self.min_y or other_cube.y > self.max_y:
                        continue

                    if other_cube.z < self.min_z or other_cube.z > self.max_z:
                        continue

                    if other_cube in handled:
                        continue

                    # If we hit the edge, we're not enclosed
                    if other_cube.x == self.min_x or other_cube.x == self.max_x:
                        group.enclosed = False

                    if other_cube.y == self.min_y or other_cube.y == self.max_y:
                        group.enclosed = False

                    if other_cube.z == self.min_z or other_cube.z == self.max_z:
                        group.enclosed = False

                    q.put(other_cube)
                    group.cubes.add(other_cube)
                    handled.add(other_cube)

            groupings.append(group)

        return groupings

    def part1(self):
        result = self._get_exposed_sides(self.cubes)

        print("Part 1:", result)

    def part2(self):

        groupings = self._get_groupings()

        cubes_under_test = set(self.cubes)
        for group in groupings:
            if group.enclosed:
                cubes_under_test = cubes_under_test.union(group.cubes)

        result = self._get_exposed_sides(cubes_under_test)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2022D18("2022/18.txt")
    code.part1()
    code.part2()
