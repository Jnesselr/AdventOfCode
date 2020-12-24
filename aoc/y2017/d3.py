from aoc.util.coordinate import TurtleDirection, Turtle, Coordinate
from aoc.util.grid import MagicGrid
from aoc.util.inputs import Input


class Y2017D3(object):
    def __init__(self, file_name):
        self.input = Input(file_name).int()

    def part1(self):
        # value = self.input - 1
        # diff = 1
        #
        # turtle = Turtle(TurtleDirection.RIGHT)
        # while value > 0:
        #     if value < diff:
        #         diff = value
        #
        #     value -= diff
        #     turtle = turtle.forward(diff)
        #     turtle = turtle.turn_left()
        #     if turtle.direction in [TurtleDirection.LEFT, TurtleDirection.RIGHT]:
        #         diff += 1

        result = 0
        for _, coordinate in zip(range(self.input), self._spiral()):
            result = abs(coordinate.x) + abs(coordinate.y)

        print("Part 1:", result)

    def part2(self):
        def _magic_grid(g: MagicGrid[int], coordinate: Coordinate):
            if coordinate.x == 0 and coordinate.y == 0:
                return 1

            return sum(g[neighbor] for neighbor in coordinate.neighbors8() if neighbor in g)

        grid: MagicGrid[int]() = MagicGrid[int](_magic_grid)

        result = 0
        for coordinate in self._spiral():
            value = grid[coordinate]
            if value > self.input:
                result = value
                break

        print("Part 2:", result)

    @staticmethod
    def _spiral():
        diff = 1

        turtle = Turtle(TurtleDirection.RIGHT)
        yield turtle.coordinate
        while True:
            for _ in range(diff):
                turtle = turtle.forward()
                yield turtle.coordinate
            turtle = turtle.turn_left()
            if turtle.direction in [TurtleDirection.LEFT, TurtleDirection.RIGHT]:
                diff += 1


if __name__ == '__main__':
    code = Y2017D3("2017/3.txt")
    code.part1()
    code.part2()
