import re
from collections import Counter
from dataclasses import dataclass
from typing import Optional, Dict

from aoc.util.inputs import Input


@dataclass(frozen=True)
class Cube(object):
    min_x: int
    max_x: int
    min_y: int
    max_y: int
    min_z: int
    max_z: int

    def intersect(self, other: 'Cube') -> Optional['Cube']:
        result = Cube(
            min_x=max(self.min_x, other.min_x),
            max_x=min(self.max_x, other.max_x),
            min_y=max(self.min_y, other.min_y),
            max_y=min(self.max_y, other.max_y),
            min_z=max(self.min_z, other.min_z),
            max_z=min(self.max_z, other.max_z),
        )

        if result.min_x <= result.max_x and result.min_y <= result.max_y and result.min_z <= result.max_z:
            return result
        else:
            return None

    @property
    def volume(self):
        return (self.max_x - self.min_x + 1) * (self.max_y - self.min_y + 1) * (self.max_z - self.min_z + 1)


class Y2021D22(object):
    command_regex = re.compile(r'(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)')

    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self._cubes: Dict[Cube, bool] = {}  # Assumes ordered dictionary which is true as of python 3.7

        for line in lines:
            match = self.command_regex.match(line)
            turn_on: bool = match.group(1) == "on"
            cube = Cube(
                min_x=int(match.group(2)),
                max_x=int(match.group(3)),
                min_y=int(match.group(4)),
                max_y=int(match.group(5)),
                min_z=int(match.group(6)),
                max_z=int(match.group(7))
            )
            self._cubes[cube] = turn_on

    def part1(self):
        boundary: Cube = Cube(-50, 50, -50, 50, -50, 50)
        cubes: Dict[Cube, bool] = dict([(cube.intersect(boundary), value) for cube, value in self._cubes.items()])
        cubes: Dict[Cube, bool] = dict((key, value) for key, value in cubes.items() if key is not None)
        result = self._cube_count(cubes)

        print("Part 1:", result)

    def part2(self):
        result = self._cube_count(self._cubes)

        print("Part 2:", result)

    # Based on https://en.wikipedia.org/wiki/Inclusion–exclusion_principle
    @staticmethod
    def _cube_count(cubes: Dict[Cube, bool]) -> int:
        all_cubes: Counter[Cube, int] = Counter()

        for cube, is_on in cubes.items():
            updated_cubes = Counter()
            for other_cube, sign in all_cubes.items():
                intersection = cube.intersect(other_cube)
                if intersection is not None:
                    # All the removals get added back and all the additions get removed. It's a reset to off for any
                    # overlap with our cube.
                    updated_cubes[intersection] -= sign

            if is_on:
                updated_cubes[cube] += 1  # Make sure to count the cube if it's on

            # This method is why we need the Counter. dict replaces values, Counter adds them.
            all_cubes.update(updated_cubes)

        return sum(cube.volume * sign for cube, sign in all_cubes.items())


if __name__ == '__main__':
    code = Y2021D22("2021/22.txt")
    code.part1()
    code.part2()
