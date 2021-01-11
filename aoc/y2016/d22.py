import itertools
import re

from aoc.util.coordinate import Coordinate, CoordinateSystem
from aoc.util.grid import InfiniteGrid
from aoc.util.inputs import Input


class Y2016D22(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.size = {}
        self.used = {}
        self.avail = {}
        self.coordinates = {}
        self.nodes = set()

        for line in lines[2:]:
            matched = re.match(r'([\w\d/-]+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)%', line)
            name = matched.group(1)
            self.nodes.add(name)
            self.size[name] = int(matched.group(2))
            self.used[name] = int(matched.group(3))
            self.avail[name] = int(matched.group(4))

            name_match = re.match(r'/dev/grid/node-x(\d+)-y(\d+)', name)
            self.coordinates[name] = Coordinate(
                x=int(name_match.group(1)),
                y=int(name_match.group(2)),
                system=CoordinateSystem.X_RIGHT_Y_DOWN
            )

    def part1(self):
        result = 0

        for a, b in itertools.product(self.nodes, repeat=2):
            if a == b:
                continue

            if self.used[a] == 0:
                continue

            if self.used[a] > self.avail[b]:
                continue

            result += 1

        print("Part 1:", result)

    def part2(self):
        grid = self._get_grid()
        grid.print()
        empty_node = [name for name, used in self.used.items() if used == 0].pop()
        empty_coordinate = self.coordinates[empty_node]
        top_right_coordinate = max(
            [coordinate for coordinate in self.coordinates.values() if coordinate.y == 0],
            key=lambda coordinate: coordinate.x
        )

        # Move the empty spot to the cell left of the top right one
        path = grid.find_path(empty_coordinate, top_right_coordinate.left(), '.')

        result = len(path) - 1
        # The 5x is right, down, left, left, up. Essentially moves the goal data one to the left,
        # and then moves the empty cell around to the left of the new cell with our goal data.
        # The +1 is for the last move to the right which moves our goal data into our target cell.
        result += 5 * (grid.width - 2) + 1

        print("Part 2:", result)

    def _get_grid(self):
        grid = InfiniteGrid[str]()

        x = y = 0
        while True:
            if f"/dev/grid/node-x0-y{y}" not in self.nodes:
                break
            while True:
                name = f"/dev/grid/node-x{x}-y{y}"
                if name not in self.nodes:
                    break

                # Hardcoded value, might need to be changed for other data.
                grid[x, y] = '.' if self.size[name] < 500 else '#'

                x += 1

            x = 0
            y += 1

        return grid.to_grid()


if __name__ == '__main__':
    code = Y2016D22("2016/22.txt")
    code.part1()
    code.part2()
