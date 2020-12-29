from enum import Enum, auto
from itertools import product

from aoc.util.coordinate import Turtle, TurtleDirection, Coordinate, CoordinateSystem
from aoc.util.grid import InfiniteGrid
from aoc.util.inputs import Input


class NodeType(Enum):
    Clean = auto()
    Infected = auto()
    Weakened = auto()
    Flagged = auto()


class Y2017D22(object):
    def __init__(self, file_name):
        initial_grid = Input(file_name).grid()
        self.grid = InfiniteGrid[NodeType]()

        center_x = center_y = initial_grid.width // 2
        for x, y in product(range(initial_grid.width), repeat=2):
            self.grid[x - center_x, y - center_y] = NodeType.Infected if initial_grid[x, y] == '#' else NodeType.Clean

    def part1(self):
        grid: InfiniteGrid[bool] = self.grid.copy()
        cleaner = Turtle(
            direction=TurtleDirection.NORTH,
            coordinate=Coordinate(0, 0, system=CoordinateSystem.X_RIGHT_Y_DOWN)
        )
        result = 0

        for _ in range(10_000):
            clean = grid[cleaner.coordinate] in [None, NodeType.Clean]

            cleaner = cleaner.turn_left() if clean else cleaner.turn_right()
            grid[cleaner.coordinate] = NodeType.Infected if clean else NodeType.Clean

            result += 1 if clean else 0

            cleaner = cleaner.forward()

        print("Part 1:", result)

    def part2(self):
        grid: InfiniteGrid[bool] = self.grid.copy()
        cleaner = Turtle(
            direction=TurtleDirection.NORTH,
            coordinate=Coordinate(0, 0, system=CoordinateSystem.X_RIGHT_Y_DOWN)
        )
        result = 0

        for _ in range(10_000_000):
            node_type = grid[cleaner.coordinate]
            if node_type is None:
                node_type = NodeType.Clean

            if node_type == NodeType.Clean:
                cleaner = cleaner.turn_left()
                grid[cleaner.coordinate] = NodeType.Weakened
            elif node_type == NodeType.Weakened:
                result += 1
                grid[cleaner.coordinate] = NodeType.Infected
            elif node_type == NodeType.Infected:
                cleaner = cleaner.turn_right()
                grid[cleaner.coordinate] = NodeType.Flagged
            else:
                cleaner = cleaner.turn_left(2)
                grid[cleaner.coordinate] = NodeType.Clean

            cleaner = cleaner.forward()

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2017D22("2017/22.txt")
    code.part1()
    code.part2()
