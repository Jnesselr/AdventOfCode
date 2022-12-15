from aoc.util.coordinate import Coordinate, CoordinateSystem
from aoc.util.grid import InfiniteGrid
from aoc.util.inputs import Input


class Y2022D14(object):
    air = '.'
    rock = '#'
    sand = 'o'

    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.base_grid: InfiniteGrid[str] = InfiniteGrid[str]()

        for line in lines:
            line_split = line.split(' -> ')
            for i in range(len(line_split) - 1):
                a, b = line_split[i], line_split[i + 1]
                a_x, a_y = a.split(',')
                b_x, b_y = b.split(',')
                a_x = int(a_x)
                a_y = int(a_y)
                b_x = int(b_x)
                b_y = int(b_y)

                if b_x < a_x or b_y < a_y:  # Swap a and b coordinates
                    a_x, a_y, b_x, b_y = b_x, b_y, a_x, a_y

                for x in range(a_x, b_x + 1):
                    for y in range(a_y, b_y + 1):
                        self.base_grid[x, y] = self.rock

        # self.base_grid.to_grid().print(not_found=self.air)

    def _fill_with_sand(self, grid: InfiniteGrid[str]):
        _sand_start = Coordinate(500, 0, system=CoordinateSystem.X_RIGHT_Y_DOWN)

        max_y = grid.max_y
        while True:
            sand_particle = _sand_start

            if _sand_start in grid:
                return  # Nowhere to go

            at_rest = False
            while not at_rest:
                if sand_particle.y > max_y:
                    return  # Exit our entire loop if this particle made it below our max y

                sand_down = sand_particle.down()
                if sand_down not in grid:
                    sand_particle = sand_down
                    continue  # Nothing underneath, drop and continue

                sand_down_left = sand_down.left()
                if sand_down_left not in grid:
                    sand_particle = sand_down_left
                    continue  # Nothing down and to the left, go there and continue

                sand_down_right = sand_down.right()
                if sand_down_right not in grid:
                    sand_particle = sand_down_right
                    continue  # Nothing down and to the right, go there and continue

                # At this point, we didn't move
                at_rest = True
                grid[sand_particle] = self.sand
                # self.base_grid.to_grid().print(not_found=self.air)
                # print()

    def part1(self):
        grid = self.base_grid.copy()
        self._fill_with_sand(grid)
        result = len(grid.find(self.sand))

        print("Part 1:", result)

    def part2(self):
        grid = self.base_grid.copy()
        max_y = grid.max_y

        for x in range(-max_y - 5, max_y + 5):
            grid[500 + x, max_y + 2] = '#'

        self._fill_with_sand(grid)
        # grid.to_grid().print()

        result = len(grid.find(self.sand))

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2022D14("2022/14.txt")
    code.part1()
    code.part2()
