import itertools

from aoc.util.coordinate import Coordinate, Turtle, TurtleDirection
from aoc.util.grid import Grid
from aoc.util.inputs import Input


class Animal:
    def __init__(self, grid: Grid[str], turtle: Turtle):
        self._turtle = turtle
        self._grid = grid

    @property
    def coordinate(self) -> Coordinate:
        return self._turtle.coordinate

    def step(self):
        self._turtle = self._turtle.forward()

        grid_item = self._grid[self._turtle.coordinate]
        if self._turtle.direction == TurtleDirection.NORTH:
            if grid_item == '7':
                self._turtle = self._turtle.turn_left()
            elif grid_item == 'F':
                self._turtle = self._turtle.turn_right()
            elif grid_item == '|':
                pass  # Nothing to do
            else:
                raise ValueError("Unexpected tile in animal path")
        elif self._turtle.direction == TurtleDirection.SOUTH:
            if grid_item == 'L':
                self._turtle = self._turtle.turn_left()
            elif grid_item == 'J':
                self._turtle = self._turtle.turn_right()
            elif grid_item == '|':
                pass  # Nothing to do
            else:
                raise ValueError("Unexpected tile in animal path")
        elif self._turtle.direction == TurtleDirection.EAST:
            if grid_item == 'J':
                self._turtle = self._turtle.turn_left()
            elif grid_item == '7':
                self._turtle = self._turtle.turn_right()
            elif grid_item == '-':
                pass  # Nothing to do
            else:
                raise ValueError("Unexpected tile in animal path")
        elif self._turtle.direction == TurtleDirection.WEST:
            if grid_item == 'F':
                self._turtle = self._turtle.turn_left()
            elif grid_item == 'L':
                self._turtle = self._turtle.turn_right()
            elif grid_item == '-':
                pass  # Nothing to do
            else:
                raise ValueError("Unexpected tile in animal path")


class Y2023D10(object):
    def __init__(self, file_name):
        grid = Input(file_name).grid()

        # Start by finding the coordinate where the animal starts
        start_coordinate = grid.find('S')[0]

        # Then find what sections of the loop lead into that tile
        north = south = east = west = False
        animal = None

        if str(grid[start_coordinate.up()] or 'NONE') in '|7F':
            north = True
            animal = Animal(grid, turtle=Turtle(
                direction=TurtleDirection.UP,
                coordinate=start_coordinate
            ))
        if str(grid[start_coordinate.down()] or 'NONE') in '|LJ':
            south = True
            animal = Animal(grid, turtle=Turtle(
                direction=TurtleDirection.DOWN,
                coordinate=start_coordinate
            ))
        if str(grid[start_coordinate.left()] or 'NONE') in '-LF':
            west = True
            animal = Animal(grid, turtle=Turtle(
                direction=TurtleDirection.LEFT,
                coordinate=start_coordinate
            ))
        if str(grid[start_coordinate.right()] or 'NONE') in '-J7':
            east = True
            animal = Animal(grid, turtle=Turtle(
                direction=TurtleDirection.RIGHT,
                coordinate=start_coordinate
            ))

        # Based on what tiles lead into this one, replace the start with the correct tile
        if north and south:
            grid[start_coordinate] = '|'
        elif east and west:
            grid[start_coordinate] = '-'
        elif north and east:
            grid[start_coordinate] = 'L'
        elif north and west:
            grid[start_coordinate] = 'J'
        elif south and west:
            grid[start_coordinate] = '7'
        elif south and east:
            grid[start_coordinate] = 'F'
        else:
            raise ValueError("Cannot determine animal starting point replacement")

        # Next we'll have the animal travel our loop
        self._loop_coordinates: set[Coordinate] = set()
        while animal.coordinate not in self._loop_coordinates:
            self._loop_coordinates.add(animal.coordinate)
            animal.step()

        # Part 1 is just halfway around that loop
        # For part 2, we need to scale the box up twice as big. This makes small gaps equal to one tile big.

        # Anything that's not in the loop becomes ground. This is mostly a cleanup step for visualization and for making
        # sure we can easily test for pieces inside/outside the loop.
        for coordinate in grid:
            if coordinate in self._loop_coordinates:
                continue

            grid[coordinate] = '.'

        # print("Single Grid")
        # grid.print()
        # print()

        # Now we make that double sized grid
        double_grid: Grid[str] = Grid(grid.width * 2, grid.height * 2)
        double_grid.fill('.')

        for coordinate in self._loop_coordinates:
            tile = grid[coordinate]

            double_coord = coordinate * 2
            double_grid[double_coord] = tile  # Get the obvious one out of the way

            if tile in '|LJ':
                double_grid[double_coord.up()] = '|'
            if tile in '|7F':
                double_grid[double_coord.down()] = '|'
            if tile in '-LF':
                double_grid[double_coord.right()] = '-'
            if tile in '-J7':
                double_grid[double_coord.left()] = '-'

        # Now found all the tiles with '.'. We're guaranteed to be connected to the outside now or be totally inside the
        # loop. We make an assumption that the '.' tiles on each edge will be sufficient to connect everything but not
        # necessarily that any one of those tiles will connect to all of them.

        for coordinate in double_grid.find('.'):
            if not coordinate.x == 0 and \
                    not coordinate.y == 0 and \
                    not coordinate.x == double_grid.width - 1 and \
                    not coordinate.y == double_grid.height - 1:
                continue  # Not on the edge, don't want to risk grabbing an inside one

            if double_grid[coordinate] != '.':  # Changed by a previous flood fill
                continue

            double_grid.flood_fill(coordinate, '.', 'O')

        # Great, now anything with a '.' is inside, but we have to scale back down. We can do that by finding all of
        # them, and then only counting the even ones.

        for coordinate in double_grid.find('.'):
            if coordinate.x % 2 != 0 or coordinate.y % 2 != 0:
                continue

            double_grid[coordinate] = 'I'

        # Now we just count the "I"'s and that's how many enclosed ones there are
        self._enclosed = len(double_grid.find('I'))

        # print("Double Grid")
        # double_grid.print()
        # print()

    def part1(self):
        result = len(self._loop_coordinates) // 2

        print("Part 1:", result)

    def part2(self):
        result = self._enclosed

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2023D10("2023/10.txt")
    code.part1()
    code.part2()
