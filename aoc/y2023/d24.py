import re
from dataclasses import dataclass
from itertools import permutations, combinations
from typing import Optional

from z3 import Solver, Int, And

from aoc.util.inputs import Input


@dataclass(frozen=True)
class CoordinateF:
    x: float
    y: float


@dataclass(frozen=True)
class Hailstone:
    x: int
    y: int
    z: int
    vx: int
    vy: int
    vz: int

    def __repr__(self) -> str:
        return f"{self.x}, {self.y}, {self.z} @ {self.vx}, {self.vy}, {self.vz}"

    def intersection(self, other: 'Hailstone') -> Optional[CoordinateF]:
        denominator = (other.vx * self.vy - other.vy * self.vx)
        if denominator == 0:
            return None

        t = (self.vy * (self.x - other.x) - self.vx * (self.y - other.y)) / denominator
        if t < 0:
            return None

        s = (other.x + (other.vx * t) - self.x) / self.vx
        if s < 0:
            return None

        return CoordinateF(
            x=other.x + t * other.vx,
            y=other.y + t * other.vy
        )


class Y2023D24(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()

        line_re = re.compile(r'(-?\d+),\s+(-?\d+),\s+(-?\d+)\s+@\s+(-?\d+),\s+(-?\d+),\s+(-?\d+)')
        self.hailstones: list[Hailstone] = []
        for line in lines:
            match = line_re.match(line)
            self.hailstones.append(Hailstone(
                x=int(match.group(1)),
                y=int(match.group(2)),
                z=int(match.group(3)),
                vx=int(match.group(4)),
                vy=int(match.group(5)),
                vz=int(match.group(6)),
            ))

    def part1(self):
        result = 0

        min_value = 200000000000000
        max_value = 400000000000000
        for a, b in combinations(self.hailstones, 2):
            intersection = a.intersection(b)
            if intersection is None:
                continue
            if min_value < intersection.x < max_value and min_value < intersection.y < max_value:
                result += 1

        print("Part 1:", result)

    def part2(self):
        # I don't remember how to solve this system of equations, so Z3 to the rescue
        s = Solver()

        rock_x = Int("x")
        rock_y = Int("y")
        rock_z = Int("z")
        rock_vx = Int("vx")
        rock_vy = Int("vy")
        rock_vz = Int("vz")

        for index, hailstone in enumerate(self.hailstones):
            time = Int(f"time_{index}")
            s.add(And(
                hailstone.x + hailstone.vx * time == rock_x + rock_vx * time,
                hailstone.y + hailstone.vy * time == rock_y + rock_vy * time,
                hailstone.z + hailstone.vz * time == rock_z + rock_vz * time,
            ))

        s.check()
        model = s.model()
        result = model[rock_x].as_long() + model[rock_y].as_long() + model[rock_z].as_long()

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2023D24("2023/24.txt")
    code.part1()
    code.part2()
