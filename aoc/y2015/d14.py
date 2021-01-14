import re
from dataclasses import dataclass

from aoc.util.inputs import Input


@dataclass(frozen=True)
class Reindeer(object):
    name: str
    speed: int
    timeout: int
    rest: int

    def distance_at(self, time):
        mod_time = time % (self.timeout + self.rest)
        quotient = time // (self.timeout + self.rest)

        distance = quotient * self.speed * self.timeout
        distance += min(self.timeout, mod_time) * self.speed

        return distance


class Y2015D14(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()

        self.reindeers = set()
        regex = re.compile(r'(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.')
        for line in lines:
            matched = regex.match(line)
            name = matched.group(1)
            speed = int(matched.group(2))
            timeout = int(matched.group(3))
            rest = int(matched.group(4))
            self.reindeers.add(Reindeer(name, speed, timeout, rest))

    def part1(self):
        result = 0

        for reindeer in self.reindeers:
            result = max(result, reindeer.distance_at(2503))

        print("Part 1:", result)

    def part2(self):
        points = {}

        for time in range(1, 2504):
            distances = dict((reindeer.name, reindeer.distance_at(time)) for reindeer in self.reindeers)
            max_value = max(distances.values())

            for name, value in distances.items():
                if value != max_value:
                    continue

                points[name] = points.setdefault(name, 0) + 1

        result = max(points.values())

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2015D14("2015/14.txt")
    code.part1()
    code.part2()
