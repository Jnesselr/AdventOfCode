from queue import Queue

from aoc.util.coordinate import Coordinate, TurtleDirection, Turtle, CoordinateSystem
from aoc.util.inputs import Input


class Y2023D16(object):
    def __init__(self, file_name):
        self.grid = Input(file_name).grid()

    def part1(self):
        initial = Turtle(
            direction=TurtleDirection.RIGHT,
            coordinate=Coordinate(0, 0, CoordinateSystem.X_RIGHT_Y_DOWN)
        )

        result = self._get_energized(initial)

        print("Part 1:", result)

    def part2(self):
        result = 0

        for row in range(self.grid.height):
            result = max(result, self._get_energized(Turtle(
                direction=TurtleDirection.RIGHT,
                coordinate=Coordinate(0, row, CoordinateSystem.X_RIGHT_Y_DOWN)
            )))
            result = max(result, self._get_energized(Turtle(
                direction=TurtleDirection.LEFT,
                coordinate=Coordinate(self.grid.width - 1, row, CoordinateSystem.X_RIGHT_Y_DOWN)
            )))

        for col in range(self.grid.width):
            result = max(result, self._get_energized(Turtle(
                direction=TurtleDirection.DOWN,
                coordinate=Coordinate(col, 0, CoordinateSystem.X_RIGHT_Y_DOWN)
            )))
            result = max(result, self._get_energized(Turtle(
                direction=TurtleDirection.UP,
                coordinate=Coordinate(col, self.grid.height - 1, CoordinateSystem.X_RIGHT_Y_DOWN)
            )))

        print("Part 2:", result)

    def _get_energized(self, initial: Turtle):
        grid = self.grid.copy()

        seen: set[Turtle] = set()
        q = Queue()
        q.put(initial)
        while not q.empty():
            turtle: Turtle = q.get()
            if turtle.coordinate not in grid:
                continue

            grid[turtle.coordinate] = '#'

            if turtle in seen:
                continue

            seen.add(turtle)

            value = self.grid[turtle.coordinate]
            if turtle.direction in [TurtleDirection.LEFT, TurtleDirection.RIGHT]:
                if value == '/':
                    q.put(turtle.turn_left().forward())
                elif value == '\\':
                    q.put(turtle.turn_right().forward())
                elif value == '|':
                    q.put(turtle.turn_left().forward())
                    q.put(turtle.turn_right().forward())
                else:
                    q.put(turtle.forward())
            else:  # Up or Down
                if value == '/':
                    q.put(turtle.turn_right().forward())
                elif value == '\\':
                    q.put(turtle.turn_left().forward())
                elif value == '-':
                    q.put(turtle.turn_left().forward())
                    q.put(turtle.turn_right().forward())
                else:
                    q.put(turtle.forward())

        return len(grid.find('#'))


if __name__ == '__main__':
    code = Y2023D16("2023/16.txt")
    code.part1()
    code.part2()
