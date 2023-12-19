from dataclasses import dataclass

from aoc.util.coordinate import Coordinate, TurtleDirection, CoordinateSystem
from aoc.util.graph import Graph, Heuristic
from aoc.util.inputs import Input


@dataclass(frozen=True)
class CoordinatedDirection:
    coordinate: Coordinate
    direction: TurtleDirection


class CoordinatedDirectionHeuristic(Heuristic[CoordinatedDirection]):
    def __call__(self, start: CoordinatedDirection, end: CoordinatedDirection) -> int:
        return end.coordinate.manhattan(start.coordinate)


class Y2023D17(object):
    def __init__(self, file_name):
        self.grid = Input(file_name).grid()

    def part1(self):
        result = self._get_path_cost(1, 3)

        print("Part 1:", result)

    def part2(self):
        result = self._get_path_cost(4, 10)

        print("Part 2:", result)

    def _get_path_cost(self, min_step: int, max_step: int) -> int:
        graph: Graph[CoordinatedDirection] = Graph(directional=True)

        # Each step jumps from our current facing direction to the next turn, counting the loss along the way
        for step in range(min_step, max_step + 1):
            for coordinate in self.grid:
                right = coordinate.right(step)
                left = coordinate.left(step)
                up = coordinate.up(step)
                down = coordinate.down(step)

                if up in self.grid:
                    up_value = sum(int(self.grid[coordinate.up(i + 1)]) for i in range(step))
                    graph.add(
                        start=CoordinatedDirection(coordinate=coordinate, direction=TurtleDirection.UP),
                        end=CoordinatedDirection(coordinate=up, direction=TurtleDirection.RIGHT),
                        weight=up_value
                    )

                    graph.add(
                        start=CoordinatedDirection(coordinate=coordinate, direction=TurtleDirection.UP),
                        end=CoordinatedDirection(coordinate=up, direction=TurtleDirection.LEFT),
                        weight=up_value
                    )

                if down in self.grid:
                    down_value = sum(int(self.grid[coordinate.down(i + 1)]) for i in range(step))
                    graph.add(
                        start=CoordinatedDirection(coordinate=coordinate, direction=TurtleDirection.DOWN),
                        end=CoordinatedDirection(coordinate=down, direction=TurtleDirection.RIGHT),
                        weight=down_value
                    )
                    graph.add(
                        start=CoordinatedDirection(coordinate=coordinate, direction=TurtleDirection.DOWN),
                        end=CoordinatedDirection(coordinate=down, direction=TurtleDirection.LEFT),
                        weight=down_value
                    )

                if left in self.grid:
                    left_value = sum(int(self.grid[coordinate.left(i + 1)]) for i in range(step))
                    graph.add(
                        start=CoordinatedDirection(coordinate=coordinate, direction=TurtleDirection.LEFT),
                        end=CoordinatedDirection(coordinate=left, direction=TurtleDirection.UP),
                        weight=left_value
                    )
                    graph.add(
                        start=CoordinatedDirection(coordinate=coordinate, direction=TurtleDirection.LEFT),
                        end=CoordinatedDirection(coordinate=left, direction=TurtleDirection.DOWN),
                        weight=left_value
                    )

                if right in self.grid:
                    right_value = sum(int(self.grid[coordinate.right(i + 1)]) for i in range(step))
                    graph.add(
                        start=CoordinatedDirection(coordinate=coordinate, direction=TurtleDirection.RIGHT),
                        end=CoordinatedDirection(coordinate=right, direction=TurtleDirection.UP),
                        weight=right_value
                    )
                    graph.add(
                        start=CoordinatedDirection(coordinate=coordinate, direction=TurtleDirection.RIGHT),
                        end=CoordinatedDirection(coordinate=right, direction=TurtleDirection.DOWN),
                        weight=right_value
                    )

        # Make an artificial endpoint
        fake_end = CoordinatedDirection(
            coordinate=Coordinate(self.grid.width, self.grid.height, CoordinateSystem.X_RIGHT_Y_DOWN),
            # Not a valid coordinate
            direction=TurtleDirection.RIGHT,  # Arbitrary
        )

        real_end_coordinate = Coordinate(self.grid.width - 1, self.grid.height - 1, CoordinateSystem.X_RIGHT_Y_DOWN)

        # We can be coming from above and turn right/left or from the left and turn up/down. To reduce the number of
        # possibilities a little, we only need to account for one set of left or right and one set of up or down.
        graph.add(
            start=CoordinatedDirection(coordinate=real_end_coordinate, direction=TurtleDirection.RIGHT),
            end=fake_end,
            weight=0
        )
        graph.add(
            start=CoordinatedDirection(coordinate=real_end_coordinate, direction=TurtleDirection.DOWN),
            end=fake_end,
            weight=0
        )

        # We can either start moving right or start moving down, but we don't know which
        start_right = CoordinatedDirection(
            coordinate=(Coordinate(0, 0, system=CoordinateSystem.X_RIGHT_Y_DOWN)),
            direction=TurtleDirection.RIGHT
        )
        start_down = CoordinatedDirection(
            coordinate=(Coordinate(0, 0, system=CoordinateSystem.X_RIGHT_Y_DOWN)),
            direction=TurtleDirection.DOWN
        )
        start = CoordinatedDirection(
            coordinate=Coordinate(-1, -1, system=CoordinateSystem.X_RIGHT_Y_DOWN),  # Not a valid coordinate
            direction=TurtleDirection.RIGHT  # Arbitrary
        )
        graph.add(start=start, end=start_right, weight=0)
        graph.add(start=start, end=start_down, weight=0)

        heuristic = CoordinatedDirectionHeuristic()
        path = graph.find_path(start, fake_end, heuristic)
        return graph.get_weight(path)


if __name__ == '__main__':
    code = Y2023D17("2023/17.txt")
    code.part1()
    code.part2()
