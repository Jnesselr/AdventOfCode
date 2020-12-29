from __future__ import annotations

import math
import re
from dataclasses import dataclass

from aoc.util.inputs import Input
from aoc.util.vector import Vector


class Y2019D12(object):
    def __init__(self, file_name):
        self.lines = Input(file_name).lines()
        self.moons = []
        self.velocities = []
        self.reset()

        self._origin_vector = Vector(0, 0, 0)

    def reset(self):
        self.moons = []
        self.velocities = []
        for line in self.lines:
            matched = re.search(r'^<x=(-?\d+), y=(-?\d+), z=(-?\d+)>$', line)
            x = int(matched.group(1))
            y = int(matched.group(2))
            z = int(matched.group(3))
            self.moons.append(Vector(x, y, z))
            self.velocities.append(Vector())

    def _energy(self, vector: Vector):
        return vector.distance(self._origin_vector)

    def part1(self):
        self.reset()

        for _ in range(1000):
            self._move_one_step()

        potential = [self._energy(moon) for moon in self.moons]
        kinetic = [self._energy(velocity) for velocity in self.velocities]

        result = sum([p * k for p, k in zip(potential, kinetic)])
        print("Part 1:", result)

    def part2(self):
        self.reset()
        lcm_x = lcm_y = lcm_z = None
        original_moons = self.moons.copy()

        steps = 0
        while lcm_x is None or lcm_y is None or lcm_z is None:
            self._move_one_step()
            steps += 1

            valid_x = all(now.x == start.x for now, start in zip(self.moons, original_moons))
            valid_x &= all(now.x == 0 for now in self.velocities)

            if valid_x and lcm_x is None:
                lcm_x = steps

            valid_y = all(now.y == start.y for now, start in zip(self.moons, original_moons))
            valid_y &= all(now.y == 0 for now in self.velocities)

            if valid_y and lcm_y is None:
                lcm_y = steps

            valid_z = all(now.z == start.z for now, start in zip(self.moons, original_moons))
            valid_z &= all(now.z == 0 for now in self.velocities)

            if valid_z and lcm_z is None:
                lcm_z = steps

        # TODO Maybe upgrade to python 3.9 to use builtin lcm
        print("Part 2:", self._lcm(lcm_x, self._lcm(lcm_y, lcm_z)))

    @staticmethod
    def _lcm(x, y):
        gcd = math.gcd(x, y)
        return (x // gcd) * y

    def _move_one_step(self):
        self.velocities = [self._get_velocity(moon) + velocity for moon, velocity in zip(self.moons, self.velocities)]
        self.moons = [moon + velocity for moon, velocity in zip(self.moons, self.velocities)]

    def _get_velocity(self, source_moon: Vector):
        velocity = Vector()
        for moon in self.moons:
            velocity += (moon - source_moon).signs()

        return velocity


if __name__ == '__main__':
    code = Y2019D12("2019/12.txt")
    code.part1()
    code.part2()
