from enum import Enum

from aoc.util.coordinate import Coordinate, TurtleDirection
from aoc.util.graph import CoordinateHeuristic
from aoc.util.grid import InfiniteGrid
from aoc.util.intcode import Intcode


class Tile(Enum):
    WALL = (0, '#')
    EMPTY = (1, ' ')
    OXYGEN = (2, 'O')

    def __init__(self, tile_id, character):
        self.tile_id = tile_id
        self.character = character

    @classmethod
    def from_id(cls, _id):
        for member in cls._member_map_.values():
            if member.tile_id == _id:
                return member


class Y2019D15(object):
    def __init__(self, file_name):
        self.droid = Intcode(file_name)
        self.grid = InfiniteGrid[Tile]()

    def _map_out_grid(self):
        self.grid.clear()
        self.droid.reset()

        all_directions = [
            TurtleDirection.NORTH,
            TurtleDirection.SOUTH,
            TurtleDirection.EAST,
            TurtleDirection.WEST
        ]

        droid_coordinate = Coordinate(0, 0)
        self.grid[droid_coordinate] = Tile.EMPTY
        backtrack = []
        need_to_check = {droid_coordinate: all_directions.copy()}

        self.droid.run()
        while backtrack or need_to_check:
            test_directions = need_to_check[droid_coordinate]

            # Nowhere to move, try to go back
            if not test_directions:
                del need_to_check[droid_coordinate]
                if backtrack:
                    back = backtrack.pop()
                    self.droid.input(self._get_move_input(back))
                    self.droid.output()  # Read an output, although we know we can move back
                    droid_coordinate = back.move(droid_coordinate)
                continue

            direction = test_directions.pop()
            if backtrack and direction == backtrack[-1]:
                continue  # Don't go back, use backtrack stack for that

            self.droid.input(self._get_move_input(direction))
            output = self.droid.output()

            next_coordinate = direction.move(droid_coordinate)
            self.grid[next_coordinate] = Tile.from_id(output)
            if output != 0:
                droid_coordinate = next_coordinate
                backtrack.append(direction.opposite())
                need_to_check[droid_coordinate] = all_directions.copy()

    def _get_move_input(self, direction: TurtleDirection):
        if direction == TurtleDirection.NORTH:
            return 1
        elif direction == TurtleDirection.SOUTH:
            return 2
        elif direction == TurtleDirection.WEST:
            return 3
        elif direction == TurtleDirection.EAST:
            return 4

    def part1(self):
        self._map_out_grid()

        start = Coordinate(0, 0)
        oxygen = self.grid.find(Tile.OXYGEN)[0]
        graph = self.grid.to_graph(Tile.EMPTY, Tile.OXYGEN)
        # -1 is because path includes start and they want "steps to oxygen"
        result = len(graph.find_path(start, oxygen, CoordinateHeuristic())) - 1

        print("Part 1:", result)

    def part2(self):
        self._map_out_grid()

        empty_tiles = self.grid.find(Tile.EMPTY)

        minutes = 0
        while empty_tiles:
            oxygen = self.grid.find(Tile.OXYGEN)
            for oxygen_space in oxygen:
                for neighbor in oxygen_space.neighbors():
                    if self.grid[neighbor] == Tile.EMPTY:
                        self.grid[neighbor] = Tile.OXYGEN

            minutes += 1
            empty_tiles = self.grid.find(Tile.EMPTY)

        print("Part 2:", minutes)


if __name__ == '__main__':
    code = Y2019D15("2019/15.txt")
    code.part1()
    code.part2()
