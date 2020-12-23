from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Set, Dict

from aoc.util.coordinate import BoundingBox, Coordinate, CoordinateSystem
from aoc.util.grid import Grid, MagicGrid
from aoc.util.inputs import Input
from aoc.util.queue import PriorityQueue


class Tool(Enum):
    ClimbingGear = auto()
    Torch = auto()
    Neither = auto()


@dataclass(frozen=True)
class RescueAttempt(object):
    location: Coordinate
    tool: Tool
    minutes: int = field(compare=False)


class Y2018D22(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.depth = int(lines[0][6:])
        target_coordinates = lines[1][7:].split(",")
        self.target_x = int(target_coordinates[0])
        self.target_y = int(target_coordinates[1])

        def _erosion_level(grid: MagicGrid[int], coordinate: Coordinate) -> int:
            x = coordinate.x
            y = coordinate.y
            if x == 0 and y == 0:
                geologic_index = 0
            elif x == self.target_x and y == self.target_y:
                geologic_index = 0
            elif y == 0:
                geologic_index = x * 16807
            elif x == 0:
                geologic_index = y * 48271
            else:
                geologic_index = grid[x - 1, y] * grid[x, y - 1]

            erosion_level = (geologic_index + self.depth) % 20183

            return erosion_level

        erosion_grid: MagicGrid[int] = MagicGrid[int](_erosion_level)

        def _cave_type(_: MagicGrid[str], coordinate: Coordinate) -> str:
            erosion_level = erosion_grid[coordinate]
            if erosion_level % 3 == 0:
                return '.'
            elif erosion_level % 3 == 1:
                return '='
            elif erosion_level % 3 == 2:
                return '|'

        self.grid: MagicGrid[str] = MagicGrid[str](_cave_type)

    def part1(self):
        result = 0

        for x in range(self.target_x+1):
            for y in range(self.target_y+1):
                value = self.grid[x, y]
                if value == '=':
                    result += 1
                if value == '|':
                    result += 2

        print("Part 1:", result)

    def part2(self):
        queue: PriorityQueue[RescueAttempt] = PriorityQueue[RescueAttempt]()
        result = 0
        seen: Dict[RescueAttempt, int] = {}

        start_attempt = RescueAttempt(location=Coordinate(0, 0, system=CoordinateSystem.X_RIGHT_Y_DOWN),
                                      tool=Tool.Torch, minutes=0)
        queue.push(start_attempt, start_attempt.minutes)

        while not queue.empty:
            attempt = queue.pop()

            if attempt.location.x == self.target_x and attempt.location.y == self.target_y:
                if attempt.tool != Tool.Torch:
                    new_minutes = attempt.minutes + 7
                    queue.push(RescueAttempt(
                        location=attempt.location,
                        tool=Tool.Torch,
                        minutes=new_minutes
                    ), new_minutes)
                    continue
                result = attempt.minutes
                break

            valid_coordinates = [c for c in attempt.location.neighbors() if c.x >= 0 and c.y >= 0]

            current_terrain = self.grid[attempt.location]
            for coordinate in valid_coordinates:
                new_terrain = self.grid[coordinate]
                new_tool = attempt.tool

                if current_terrain == '.' and new_terrain == '=':
                    new_tool = Tool.ClimbingGear
                elif current_terrain == '.' and new_terrain == '|':
                    new_tool = Tool.Torch
                elif current_terrain == '=' and new_terrain == '.':
                    new_tool = Tool.ClimbingGear
                elif current_terrain == '=' and new_terrain == '|':
                    new_tool = Tool.Neither
                elif current_terrain == '|' and new_terrain == '.':
                    new_tool = Tool.Torch
                elif current_terrain == '|' and new_terrain == '=':
                    new_tool = Tool.Neither

                next_attempt_minutes = attempt.minutes + 1
                if attempt.tool != new_tool:
                    next_attempt_minutes += 7  # 7 minutes just to change your tools, wow

                new_attempt = RescueAttempt(location=coordinate, tool=new_tool, minutes=next_attempt_minutes)
                if new_attempt in seen:
                    seen_minutes = seen[new_attempt]
                    if seen_minutes > next_attempt_minutes:
                        seen[new_attempt] = next_attempt_minutes
                        queue.push(new_attempt, new_attempt.minutes)
                else:
                    seen[new_attempt] = next_attempt_minutes
                    queue.push(new_attempt, new_attempt.minutes)

        self.grid.to_grid().print()
        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2018D22("2018/22.txt")
    code.part1()
    code.part2()
