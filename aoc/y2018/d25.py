from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from functools import reduce
from typing import Tuple, List, NewType

from aoc.util.inputs import Input

Point = NewType('point', Tuple[int, int, int, int])


@dataclass(frozen=True)
class Constellation(object):
    id: str = field(default_factory=lambda: uuid.uuid4().hex, hash=True)
    points: List[Point] = field(default_factory=lambda: [], hash=False)

    def __contains__(self, item: Point):
        for points in self.points:
            distance = abs(item[0] - points[0]) + \
                       abs(item[1] - points[1]) + \
                       abs(item[2] - points[2]) + \
                       abs(item[3] - points[3])

            if distance <= 3:
                return True
        return False

    def join(self, other: Constellation) -> Constellation:
        self.points.extend(other.points)

        return self


class Y2018D25(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.coordinates: List[Point] = []

        for line in lines:
            coordinate = [int(x) for x in line.split(',')]
            point = Point((coordinate[0], coordinate[1], coordinate[2], coordinate[3]))
            self.coordinates.append(point)

    def part1(self):
        constellations = set()

        for coordinate in self.coordinates:
            matching_constellations = [c for c in constellations if coordinate in c]

            if len(matching_constellations) == 0:
                constellation = Constellation()
                constellation.points.append(coordinate)
                constellations.add(constellation)
            elif len(matching_constellations) >= 1:
                constellation = reduce(lambda acc, cur: acc.join(cur), matching_constellations)
                constellation.points.append(coordinate)
                for value in matching_constellations:
                    if value.id != constellation.id:
                        constellations.remove(value)

        result = len(constellations)

        print("Part 1:", result)

    def part2(self):
        pass


if __name__ == '__main__':
    code = Y2018D25("2018/25.txt")
    code.part1()
    code.part2()
