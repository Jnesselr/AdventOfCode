import re
from dataclasses import dataclass
from typing import List, Tuple

from aoc.util.inputs import Input
from aoc.util.vector import Vector


@dataclass(frozen=True)
class Particle(object):
    position: Vector
    velocity: Vector
    acceleration: Vector

    def position_at(self, time: int) -> Vector:
        triangle_sum = (time * (time + 1)) // 2
        return self.position + (self.velocity * time) + (self.acceleration * triangle_sum)


class Y2017D20(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.particles: List[Particle] = []

        regex = re.compile(r'p=<(-?\d+),(-?\d+),(-?\d+)>, v=<(-?\d+),(-?\d+),(-?\d+)>, a=<(-?\d+),(-?\d+),(-?\d+)>')

        for line in lines:
            matched = re.match(regex, line)
            self.particles.append(Particle(
                position=Vector(
                    x=int(matched.group(1)),
                    y=int(matched.group(2)),
                    z=int(matched.group(3))
                ),
                velocity=Vector(
                    x=int(matched.group(4)),
                    y=int(matched.group(5)),
                    z=int(matched.group(6))
                ),
                acceleration=Vector(
                    x=int(matched.group(7)),
                    y=int(matched.group(8)),
                    z=int(matched.group(9))
                )
            ))

    def part1(self):
        new_positions: List[Tuple[int, Vector]] = [
            (index, self.particles[index].position_at(1000)) for index in range(len(self.particles))
        ]
        sorted_positions = sorted(new_positions, key=lambda x: abs(x[1]).distance(Vector(0, 0, 0)))
        result: int = sorted_positions[0][0]

        print("Part 1:", result)

    def part2(self):
        all_particles = set(self.particles)

        for time in range(50):
            particles_by_time = {}

            for particle in self.particles:
                particles_by_time.setdefault(particle.position_at(time), set()).add(particle)

            collided_particles = set()

            for group, value in particles_by_time.items():
                particles = set(value)
                if len(particles) > 1:
                    collided_particles = collided_particles.union(particles)

            all_particles = all_particles.difference(collided_particles)

        result = len(all_particles)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2017D20("2017/20.txt")
    code.part1()
    code.part2()
