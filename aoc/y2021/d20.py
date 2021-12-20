from aoc.util.coordinate import Coordinate, CoordinateSystem
from aoc.util.grid import Grid, InfiniteGrid
from aoc.util.inputs import Input


class Y2021D20(object):
    def __init__(self, file_name):
        groups = Input(file_name).grouped()
        self._enhancement = groups[0][0]
        self._grid = Grid.from_str(groups[1])

    def part1(self):
        grid = self._enhance_times(2)

        result = len(grid.find('#'))

        print("Part 1:", result)

    def part2(self):
        grid = self._enhance_times(50)

        result = len(grid.find('#'))

        print("Part 2:", result)

    def _enhance_times(self, times: int) -> InfiniteGrid[str]:
        grid = self._grid.copy()
        for i in range(times):
            if self._enhancement[0] == '.':
                fill = '.'
            elif self._enhancement[0] == '#' and self._enhancement[511] == '.':
                fill = '.' if i % 2 == 0 else '#'
            else:
                raise ValueError("I have no idea how to handle that")

            grid = self._enhance(grid, fill)

        return grid

    def _enhance(self, grid: InfiniteGrid[str], fill: str):
        result = InfiniteGrid[str]()

        min_x = grid.min_x - 2
        max_x = grid.max_x + 3
        min_y = grid.min_y - 2
        max_y = grid.max_y + 3
        for x in range(min_x, max_x):
            for y in range(min_y, max_y):
                coordinate = Coordinate(x, y, system=CoordinateSystem.X_RIGHT_Y_DOWN)

                if coordinate not in grid:
                    grid[coordinate] = fill

                neighbors = coordinate.neighbors8()
                for neighbor in neighbors:
                    if neighbor not in grid:
                        grid[neighbor] = fill

                bin_str = f"{grid[coordinate.up().left()]}" \
                          f"{grid[coordinate.up()]}" \
                          f"{grid[coordinate.up().right()]}" \
                          f"{grid[coordinate.left()]}" \
                          f"{grid[coordinate]}" \
                          f"{grid[coordinate.right()]}" \
                          f"{grid[coordinate.down().left()]}" \
                          f"{grid[coordinate.down()]}" \
                          f"{grid[coordinate.down().right()]}" \
                    .replace('.', '0') \
                    .replace('#', '1')
                index = int(bin_str, 2)
                result[coordinate] = self._enhancement[index]

        return result


if __name__ == '__main__':
    code = Y2021D20("2021/20.txt")
    code.part1()
    code.part2()
