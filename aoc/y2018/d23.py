from __future__ import annotations
import re
from dataclasses import dataclass
from typing import Tuple, Union

from z3 import *

from aoc.util.inputs import Input


@dataclass(frozen=True)
class Nanobot(object):
    x: int
    y: int
    z: int
    r: int

    def in_range(self, other: Union[Nanobot, Tuple[int, int, int]]) -> bool:
        return self._manhattan(other) <= self.r

    def _manhattan(self, other: Union[Nanobot, Tuple[int, int, int]]) -> int:
        if isinstance(other, Nanobot):
            other = (other.x, other.y, other.z)

        return abs(self.x - other[0]) + abs(self.y - other[1]) + abs(self.z - other[2])


class Y2018D23(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.nanobots = []

        for line in lines:
            matched = re.match(r'pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(-?\d+)', line)
            self.nanobots.append(Nanobot(
                x=int(matched.group(1)),
                y=int(matched.group(2)),
                z=int(matched.group(3)),
                r=int(matched.group(4))
            ))

    def part1(self):
        biggest: Nanobot = max(self.nanobots, key=lambda bot: bot.r)

        nanobot: Nanobot
        result = sum(1 for nanobot in self.nanobots if biggest.in_range(nanobot))

        print("Part 1:", result)

    def part2(self):
        def z3_abs(num):
            return If(num >= 0, num, -num)

        optimizer = Optimize()
        x, y, z = Ints('x y z')
        nanobots_in_range = Int('nanobots_in_range')
        distance_to_origin = Int('distance_to_origin')

        ranges = []
        for index, nanobot in enumerate(self.nanobots):
            in_range = Int(f'in_range_{index}')
            z3_range = z3_abs(x - nanobot.x) + z3_abs(y - nanobot.y) + z3_abs(z - nanobot.z)
            optimizer.add(
                in_range == If(z3_range <= nanobot.r, 1, 0)
            )
            ranges.append(in_range)
        optimizer.add(nanobots_in_range == sum(ranges))

        optimizer.add(
            distance_to_origin == z3_abs(x) + z3_abs(y) + z3_abs(z)
        )

        optimizer.maximize(nanobots_in_range)
        optimizer.minimize(distance_to_origin)

        optimizer.check()
        result = optimizer.model()[distance_to_origin]

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2018D23("2018/23.txt")
    code.part1()
    code.part2()
