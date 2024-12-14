import enum
import itertools
import re
from collections import Counter
from dataclasses import dataclass
from functools import reduce
from itertools import count
from pathlib import Path
from typing import Tuple

from PIL import Image, ImageDraw

from aoc.util.coordinate import Coordinate, CoordinateSystem
from aoc.util.inputs import Input

space_width = 101
space_height = 103
middle_x = space_width // 2
middle_y = space_height // 2


@dataclass(frozen=True)
class Robot:
    position_x: int
    position_y: int
    velocity_x: int
    velocity_y: int

    def move(self, times: int) -> 'Robot':
        return Robot(
            position_x=(self.position_x + times * self.velocity_x) % space_width,
            position_y=(self.position_y + times * self.velocity_y) % space_height,
            velocity_x=self.velocity_x,
            velocity_y=self.velocity_y,
        )


class GridQuadrant(enum.Enum):
    TOP_LEFT = enum.auto()
    TOP_RIGHT = enum.auto()
    BOTTOM_LEFT = enum.auto()
    BOTTOM_RIGHT = enum.auto()


class Y2024D14(object):
    robot_re = re.compile(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)')

    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self._robots: list[Robot] = []
        for line in lines:
            match = self.robot_re.match(line)
            self._robots.append(Robot(
                position_x=int(match.group(1)),
                position_y=int(match.group(2)),
                velocity_x=int(match.group(3)),
                velocity_y=int(match.group(4)),
            ))

    def part1(self):
        c = Counter()
        for robot in self._robots:
            robot = robot.move(100)
            if robot.position_x == middle_x or robot.position_y == middle_y:
                continue  # Ignore this robot

            if robot.position_x < middle_x and robot.position_y < middle_y:
                c[GridQuadrant.TOP_LEFT] += 1
            elif robot.position_x > middle_x and robot.position_y < middle_y:
                c[GridQuadrant.TOP_RIGHT] += 1
            elif robot.position_x < middle_x and robot.position_y > middle_y:
                c[GridQuadrant.BOTTOM_LEFT] += 1
            elif robot.position_x > middle_x and robot.position_y > middle_y:
                c[GridQuadrant.BOTTOM_RIGHT] += 1

        result = reduce(lambda x, y: x * y, c.values())
        print("Part 1:", result)

    def part2(self):
        # This is how I first found what the tree looked like and where it was.
        # self._write_out_images()

        result = 0

        for i in count(1):
            new_robots = [r.move(i) for r in self._robots]
            positions: set[Coordinate] = {
                Coordinate(x=r.position_x, y=r.position_y, system=CoordinateSystem.X_RIGHT_Y_DOWN) for r in new_robots
            }
            for coordinate in set(positions):
                has_neighbor = any([(n in positions) for n in coordinate.neighbors()])
                if not has_neighbor:
                    positions.remove(coordinate)

            # Instead of looking for the features of the tree, we just have a line where above this, we assume the tree
            # is there based on clustering. For mine, it was 363 positions that had a neighbor. That may not be the case
            # for everyone, but the highest up until now was 199 on my input which suggests 300 is a good arbitrary line
            # to draw.
            if len(positions) > 300:
                result = i
                break


        print("Part 2:", result)

    def _write_out_images(self):
        scratch_dir = Path(__file__).parent.parent.parent / "scratch" / "2024" / "14"
        scratch_dir.mkdir(parents=True, exist_ok=True)
        for i in range(0, 10000):
            img = Image.new('RGB', (space_width, space_height))
            new_robots = [r.move(i) for r in self._robots]
            for robot in new_robots:
                draw = ImageDraw.Draw(img)
                draw.point((robot.position_x, robot.position_y), (255, 255, 255, 0))

            img.save(scratch_dir / f'{i}.png', 'PNG')


if __name__ == '__main__':
    code = Y2024D14("2024/14.txt")
    code.part1()
    code.part2()
