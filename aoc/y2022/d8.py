from typing import List, Set, Callable

from aoc.util.coordinate import Coordinate, CoordinateSystem
from aoc.util.grid import Grid, InfiniteGrid
from aoc.util.inputs import Input


class Y2022D8(object):
    def __init__(self, file_name):
        self.tree_grid: InfiniteGrid[int] = Input(file_name).grid().map(lambda s: int(s))

    def part1(self):
        invisible_trees: Set[Coordinate] = set(self.tree_grid.keys())

        rows = list(range(self.tree_grid.min_x, self.tree_grid.max_x + 1))
        columns = list(range(self.tree_grid.min_y, self.tree_grid.max_y + 1))
        rows_reverse = list(rows)
        rows_reverse.reverse()
        columns_reverse = list(columns)
        columns_reverse.reverse()

        for row in rows:
            current_min_column = -1
            for col in columns:
                if current_min_column < self.tree_grid[col, row]:
                    current_min_column = self.tree_grid[col, row]
                    coordinate = Coordinate(col, row, system=CoordinateSystem.X_RIGHT_Y_DOWN)
                    if coordinate in invisible_trees:
                        invisible_trees.remove(coordinate)

            current_min_column = -1
            for col in columns_reverse:
                if current_min_column < self.tree_grid[col, row]:
                    current_min_column = self.tree_grid[col, row]
                    coordinate = Coordinate(col, row, system=CoordinateSystem.X_RIGHT_Y_DOWN)
                    if coordinate in invisible_trees:
                        invisible_trees.remove(coordinate)

        for col in columns:
            current_min_row = -1
            for row in rows:
                if current_min_row < self.tree_grid[col, row]:
                    current_min_row = self.tree_grid[col, row]
                    coordinate = Coordinate(col, row, system=CoordinateSystem.X_RIGHT_Y_DOWN)
                    if coordinate in invisible_trees:
                        invisible_trees.remove(coordinate)

            current_min_row = -1
            for row in rows_reverse:
                if current_min_row < self.tree_grid[col, row]:
                    current_min_row = self.tree_grid[col, row]
                    coordinate = Coordinate(col, row, system=CoordinateSystem.X_RIGHT_Y_DOWN)
                    if coordinate in invisible_trees:
                        invisible_trees.remove(coordinate)
        result = len(self.tree_grid.keys()) - len(invisible_trees)

        print("Part 1:", result)

    def _dist_count(self, c: Coordinate, func: Callable[[Coordinate], Coordinate]) -> int:
        initial_value = self.tree_grid[c]
        c = func(c)
        steps = 0

        while c in self.tree_grid:
            steps += 1

            if self.tree_grid[c] >= initial_value:
                return steps

            c = func(c)

        return steps

    def part2(self):
        result = 0

        for coordinate in self.tree_grid.keys():
            up_steps = self._dist_count(coordinate, lambda c: c.up())
            down_steps = self._dist_count(coordinate, lambda c: c.down())
            left_steps = self._dist_count(coordinate, lambda c: c.left())
            right_steps = self._dist_count(coordinate, lambda c: c.right())

            scenic_score = up_steps * down_steps * right_steps * left_steps
            if scenic_score > result:
                result = scenic_score

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2022D8("2022/8.txt")
    code.part1()
    code.part2()
