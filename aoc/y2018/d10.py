import re
from dataclasses import dataclass
from typing import Tuple

from aoc.util.coordinate import Coordinate, CoordinateSystem, BoundingBox
from aoc.util.grid import Grid, InfiniteGrid
from aoc.util.inputs import Input


@dataclass(frozen=True)
class Star(object):
    coordinate: Coordinate
    velocity: Tuple[int, int]

    def at(self, time: int) -> Coordinate:
        return Coordinate(
            x=self.coordinate.x + (self.velocity[0] * time),
            y=self.coordinate.y + (self.velocity[1] * time),
            system=CoordinateSystem.X_RIGHT_Y_DOWN
        )


class Y2018D10(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.stars = []

        for line in lines:
            matched = re.match(r"position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>", line)
            self.stars.append(Star(
                coordinate=Coordinate(int(matched.group(1)), int(matched.group(2)),
                                      system=CoordinateSystem.X_RIGHT_Y_DOWN),
                velocity=(int(matched.group(3)), int(matched.group(4)))
            ))

        min_time = 2**24
        max_time = 0

        for star in self.stars:
            if star.velocity[0] != 0:
                time_x = abs(star.coordinate.x // star.velocity[0])
                min_time = min(min_time, time_x)
                max_time = max(max_time, time_x)

            if star.velocity[1] != 0:
                time_y = abs(star.coordinate.y // star.velocity[1])
                min_time = min(min_time, time_y)
                max_time = max(max_time, time_y)

        min_size = 2**24
        self.best_time = 0
        for time in range(min_time, max_time+1):
            bounding_box = BoundingBox().expand(*[star.at(time) for star in self.stars])
            size = abs(bounding_box.max_y - bounding_box.min_y) * abs(bounding_box.max_x - bounding_box.min_x)

            if size < min_size:
                min_size = size
                self.best_time = time

    def part1(self):
        grid: InfiniteGrid[str] = InfiniteGrid[str]()

        for star in self.stars:
            grid[star.at(self.best_time)] = '#'

        print("Part 1:")
        grid.to_grid().print(not_found=' ')

    def part2(self):
        result = self.best_time

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2018D10("2018/10.txt")
    code.part1()
    code.part2()
