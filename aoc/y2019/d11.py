from aoc.util.coordinate import Turtle, TurtleDirection, Coordinate, CoordinateSystem
from aoc.util.grid import InfiniteGrid
from aoc.util.intcode import Intcode


class Y2019D11(object):
    def __init__(self, file_name):
        self.robot = Intcode(file_name)
        self.grid = InfiniteGrid[bool]()  # False -> black; True -> white

    def _paint(self):
        self.robot.reset()
        self.robot.run()

        turtle = Turtle(direction=TurtleDirection.UP)
        painted_tiles = set()
        while not self.robot.halted:
            if turtle.coordinate not in self.grid:
                tile_is_white = False
            else:
                tile_is_white = self.grid[turtle.coordinate]

            self.robot.input(1 if tile_is_white else 0)

            new_color = self.robot.output()

            # Paint the current tile white or black
            self.grid[turtle.coordinate] = True if new_color == 1 else False
            painted_tiles.add(turtle.coordinate)

            turn = self.robot.output()

            if turn == 0:
                turtle = turtle.turn_left()
            else:
                turtle = turtle.turn_right()

            turtle = turtle.forward()

        return painted_tiles

    def part1(self):
        self.grid.clear()
        painted_tiles = self._paint()
        result = len(painted_tiles)

        print("Part 1:", result)

    def part2(self):
        self.grid.clear()
        self.grid[Coordinate(0, 0)] = True
        self._paint()

        print("Part 2:")
        self.grid.to_grid().print(key=lambda is_white: '#' if is_white else ' ')

if __name__ == '__main__':
    code = Y2019D11("2019/11.txt")
    code.part1()
    code.part2()
