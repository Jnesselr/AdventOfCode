import re
from dataclasses import dataclass

from aoc.util.coordinate import TurtleDirection, Coordinate, CoordinateSystem
from aoc.util.inputs import Input


@dataclass
class DigPlan:
    direction: TurtleDirection
    distance: int
    rgb_hex: str

    @property
    def hex_plan(self) -> 'DigPlan':
        direction_value = self.rgb_hex[-1]
        if direction_value == '0':
            direction = TurtleDirection.RIGHT
        elif direction_value == '1':
            direction = TurtleDirection.DOWN
        elif direction_value == '2':
            direction = TurtleDirection.LEFT
        elif direction_value == '3':
            direction = TurtleDirection.UP
        else:
            raise ValueError("Invalid hex code value")

        return DigPlan(
            direction=direction,
            distance=int(self.rgb_hex[:5], 16),
            rgb_hex=self.rgb_hex
        )


class Y2023D18(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.dig_plan: list[DigPlan] = []

        line_re = re.compile(r'([LRUD]) (\d+) \(#([0-9a-z]+)\)')
        for line in lines:
            match = line_re.match(line)
            self.dig_plan.append(DigPlan(
                direction=TurtleDirection.from_direction(match.group(1)),
                distance=int(match.group(2)),
                rgb_hex=match.group(3)
            ))

    def part1(self):
        result = self._get_size_of_dig_plan(self.dig_plan)

        print("Part 1:", result)

    def part2(self):
        dig_plan = [dp.hex_plan for dp in self.dig_plan]
        result = self._get_size_of_dig_plan(dig_plan)

        print("Part 2:", result)

    @staticmethod
    def _get_size_of_dig_plan(dig_plan: list[DigPlan]) -> int:
        # Like everyone else, I used the Shoelace algorithm and Pick's theorem

        path_length = 0
        sum_a = 0
        sum_b = 0

        current_coordinate = Coordinate(1, 1, system=CoordinateSystem.X_RIGHT_Y_DOWN)

        for plan in dig_plan:
            if plan.direction == TurtleDirection.UP:
                next_coordinate = current_coordinate.up(plan.distance)
            elif plan.direction == TurtleDirection.DOWN:
                next_coordinate = current_coordinate.down(plan.distance)
            elif plan.direction == TurtleDirection.LEFT:
                next_coordinate = current_coordinate.left(plan.distance)
            elif plan.direction == TurtleDirection.RIGHT:
                next_coordinate = current_coordinate.right(plan.distance)
            else:
                raise ValueError()

            sum_a += current_coordinate.x * next_coordinate.y
            sum_b += current_coordinate.y * next_coordinate.x
            path_length += plan.distance
            current_coordinate = next_coordinate

        return abs(sum_a - sum_b) // 2 + (path_length // 2) + 1


if __name__ == '__main__':
    code = Y2023D18("2023/18.txt")
    code.part1()
    code.part2()
