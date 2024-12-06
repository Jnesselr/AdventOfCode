from tqdm import tqdm

from aoc.util.coordinate import Turtle, TurtleDirection, Coordinate
from aoc.util.inputs import Input


class Y2024D6(object):
    def __init__(self, file_name):
        self._grid = Input(file_name).grid()
        self._starting_coordinate = self._grid.find('^')[0]
        self._grid[self._starting_coordinate] = '.'

        self._valid_coordinates = set()
        turtle = Turtle(TurtleDirection.UP, self._starting_coordinate)
        while turtle.coordinate in self._grid:
            self._valid_coordinates.add(turtle.coordinate)
            new_turtle = turtle.forward()

            if self._grid[new_turtle.coordinate] == '#':
                new_turtle = turtle.turn_right()

            turtle = new_turtle

    def part1(self):
        result = len(self._valid_coordinates)

        print("Part 1:", result)

    def part2(self):
        result = 0

        for coordinate in self._valid_coordinates:
            if coordinate == self._starting_coordinate:
                continue  # Can't place an obstacle at the starting coordinate

            if self._causes_a_loop(coordinate):
                result += 1

        print("Part 2:", result)

    def _causes_a_loop(self, obstacle: Coordinate) -> bool:
        new_grid = self._grid.copy()
        new_grid[obstacle] = '#'
        known_steps = set()
        turtle = Turtle(TurtleDirection.UP, self._starting_coordinate)
        while turtle.coordinate in new_grid:
            if turtle in known_steps:  # We've seen this exact turtle before, so we'd be retracing our steps
                return True

            known_steps.add(turtle)
            new_turtle = turtle.forward()

            if new_grid[new_turtle.coordinate] == '#':
                new_turtle = turtle.turn_right()

            turtle = new_turtle

        return False


if __name__ == '__main__':
    code = Y2024D6("2024/6.txt")
    code.part1()
    code.part2()
