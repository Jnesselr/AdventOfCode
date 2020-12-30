import re

from aoc.util.grid import Grid
from aoc.util.inputs import Input


class Y2016D8(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.grid: Grid[str] = Grid(50, 6)
        self.grid.fill(' ')

        for line in lines:
            if (matched := re.match(r'rect (\d+)x(\d+)', line)) is not None:
                columns = int(matched.group(1))
                rows = int(matched.group(2))
                for row in range(rows):
                    for col in range(columns):
                        self.grid[col, row] = '#'
            elif (matched := re.match(r'rotate row y=(\d+) by (\d+)', line)) is not None:
                row_index = int(matched.group(1))
                amount = int(matched.group(2))
                row = []
                for i in range(self.grid.width):
                    row.append(self.grid[i, row_index])

                for i in range(self.grid.width):
                    self.grid[(amount + i) % self.grid.width, row_index] = row[i]
            elif (matched := re.match(r'rotate column x=(\d+) by (\d+)', line)) is not None:
                col_index = int(matched.group(1))
                amount = int(matched.group(2))
                column = []
                for i in range(self.grid.height):
                    column.append(self.grid[col_index, i])

                for i in range(self.grid.height):
                    self.grid[col_index, (i + amount) % self.grid.height] = column[i]

    def part1(self):
        result = len(self.grid.find('#'))

        print("Part 1:", result)

    def part2(self):
        print("Part 2:")

        self.grid.print(not_found='*')


if __name__ == '__main__':
    code = Y2016D8("2016/8.txt")
    code.part1()
    code.part2()
