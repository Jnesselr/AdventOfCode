from aoc.util.grid import Grid
from aoc.util.inputs import Input


class Y2020D3(object):
    def __init__(self, file_name):
        self.grid = Grid.from_str(Input(file_name).lines())

    def part1(self):
        result = self._get_slope_tree_count(3, 1)

        print("Part 1:", result)

    def part2(self):
        result = self._get_slope_tree_count(1, 1) * \
            self._get_slope_tree_count(3, 1) * \
            self._get_slope_tree_count(5, 1) * \
            self._get_slope_tree_count(7, 1) * \
            self._get_slope_tree_count(1, 2)

        print("Part 2:", result)

    def _get_slope_tree_count(self, right, down):
        result = 0
        for y in range(0, self.grid.height, down):
            x = ((y // down) * right) % self.grid.width
            if self.grid[x, y] == '#':
                result += 1
        return result


if __name__ == '__main__':
    code = Y2020D3("2020/3.txt")
    code.part1()
    code.part2()
