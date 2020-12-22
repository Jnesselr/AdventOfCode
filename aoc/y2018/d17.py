import re
from typing import Tuple, List

from aoc.util.grid import InfiniteGrid
from aoc.util.inputs import Input


class Y2018D17(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.grid = InfiniteGrid[str]()

        for line in lines:
            x_matched = re.match(r'x=(\d+), y=(\d+)..(\d+)', line)
            y_matched = re.match(r'y=(\d+), x=(\d+)..(\d+)', line)

            if x_matched is not None:
                x = int(x_matched.group(1))
                start_y = int(x_matched.group(2))
                end_y = int(x_matched.group(3))

                for y in range(start_y, end_y + 1):
                    self.grid[x, y] = '#'
            elif y_matched is not None:
                y = int(y_matched.group(1))
                start_x = int(y_matched.group(2))
                end_x = int(y_matched.group(3))

                for x in range(start_x, end_x + 1):
                    self.grid[x, y] = '#'
            else:
                raise ValueError(f"Couldn't match the line!")

        self._fill_grid_with_water()

    def part1(self):
        result = len(self.grid.find(lambda x: x in ['~', '|']))

        print("Part 1:", result)

    def part2(self):
        result = len(self.grid.find('~'))

        print("Part 2:", result)

    def _fill_grid_with_water(self):
        # Technically, it starts at 500, 0 but we don't count water outside of our bounding box
        water_spring_location = 500, self.grid.min_y - 1
        self.grid[water_spring_location] = '+'  # Water spring

        max_y = self.grid.max_y

        stack: List[Tuple] = [water_spring_location]

        while len(stack) > 0:
            water_x, water_y = stack.pop()

            if self.grid[water_x, water_y+1] is None and water_y < max_y:
                self.grid[water_x, water_y+1] = '|'
                stack.append((water_x, water_y))
                stack.append((water_x, water_y+1))
                continue
            elif self.grid[water_x, water_y + 1] in ['#', '~']:
                start_x = water_x
                end_x = water_x

                while self.grid[start_x - 1, water_y] != '#' and self.grid[start_x, water_y + 1] in ['#', '~']:
                    start_x -= 1

                while self.grid[end_x + 1, water_y] != '#' and self.grid[end_x, water_y + 1] in ['#', '~']:
                    end_x += 1

                completely_filled = True
                if self.grid[start_x, water_y + 1] in ['|', None]:
                    stack.append((start_x, water_y))
                    completely_filled = False
                if self.grid[end_x, water_y + 1] in ['|', None]:
                    stack.append((end_x, water_y))
                    completely_filled = False

                for x in range(start_x, end_x + 1):
                    self.grid[x, water_y] = '~' if completely_filled else '|'


if __name__ == '__main__':
    code = Y2018D17("2018/17.txt")
    code.part1()
    code.part2()
