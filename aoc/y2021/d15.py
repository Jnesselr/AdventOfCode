from typing import Dict, Optional

from aoc.util.coordinate import Coordinate, CoordinateSystem
from aoc.util.grid import InfiniteGrid
from aoc.util.inputs import Input
from aoc.util.queue import PriorityQueue


class Y2021D15(object):
    def __init__(self, file_name):
        self._grid: InfiniteGrid[int] = Input(file_name).grid().map(lambda x: int(x))
        # self._graph = grid.to_graph(1, 2, 3, 4, 5, 6, 7, 8, 9)
        self.start = Coordinate(
            x=self._grid.min_x,
            y=self._grid.min_y,
            system=CoordinateSystem.X_RIGHT_Y_DOWN
        )
        self.size = self._grid.max_x + 1
        self.end = Coordinate(
            x=self.size-1,
            y=self.size-1,
            system=CoordinateSystem.X_RIGHT_Y_DOWN
        )

    def part1(self):
        path = self.find_path(self._grid, self.start, self.end)
        result = sum(self._grid[x] for x in path if x != self.start)

        print("Part 1:", result)

    def part2(self):
        new_grid: InfiniteGrid[int] = self._grid.copy()

        for mult_x in range(0, 5):
            for mult_y in range(0, 5):
                if mult_x == 0 and mult_y == 0:
                    continue
                for x in range(self.size):
                    for y in range(self.size):
                        if mult_y == 0:
                            previous_x = (mult_x - 1) * self.size + x
                            previous_y = y
                        else:
                            previous_x = mult_x * self.size + x
                            previous_y = (mult_y - 1) * self.size + y

                        value = new_grid[previous_x, previous_y] + 1

                        if value > 9:
                            value = 1

                        new_grid[
                            mult_x * self.size + x,
                            mult_y * self.size + y
                        ] = value
                print()

        new_end = Coordinate(
            x=new_grid.max_x,
            y=new_grid.max_y,
            system=CoordinateSystem.X_RIGHT_Y_DOWN
        )
        path = self.find_path(new_grid, self.start, new_end)
        result = sum(new_grid[x] for x in path if x != self.start)

        print("Part 2:", result)

    def find_path(self, grid: InfiniteGrid[int],
                  start: Coordinate,
                  end: Coordinate):
        frontier: PriorityQueue[Coordinate] = PriorityQueue[Coordinate]()
        frontier.push(start, 0)
        came_from: Dict[Coordinate, Optional[Coordinate]] = {}
        cost_so_far: Dict[Coordinate, int] = {}

        came_from[start] = None
        cost_so_far[start] = 0

        while frontier:
            current: Coordinate = frontier.pop()

            if current == end:
                source = end
                result = []

                while source is not None:
                    result.insert(0, source)
                    source = came_from[source]

                return result

            for neighbor in current.neighbors():
                if neighbor not in grid:
                    continue

                # if grid[neighbor] not in walkable:
                #     continue

                new_cost = cost_so_far[current] + grid[neighbor]

                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost

                    frontier.push(neighbor, priority)
                    came_from[neighbor] = current


if __name__ == '__main__':
    code = Y2021D15("2021/15.txt")
    code.part1()
    code.part2()
