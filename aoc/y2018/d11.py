from aoc.util.grid import Grid
from aoc.util.inputs import Input


class Y2018D11(object):
    def __init__(self, file_name):
        self.serial_number = int(Input(file_name).line())
        self.grid: Grid[int] = Grid[int](300, 300)

        for x in range(300):
            for y in range(300):
                rack_id = x + 10
                power_level = rack_id * y
                power_level += self.serial_number
                power_level *= rack_id
                power_level = (power_level // 100) % 10
                power_level -= 5

                top_left = self.grid[x-1, y-1] or 0
                top = self.grid[x, y-1] or 0
                left = self.grid[x-1, y] or 0
                self.grid[x, y] = power_level + top + left - top_left

    def _get_power(self, x, y, size):
        value = self.grid[x - 1, y - 1] or 0
        bottom = self.grid[x - 1, y + size - 1] or 0
        right = self.grid[x + size - 1, y - 1] or 0
        bottom_right = self.grid[x + size - 1, y + size - 1] or 0

        return value + bottom_right - bottom - right

    def part1(self):
        result = None
        max_power = 0

        for x in range(300 - 3):
            for y in range(300 - 3):
                power = self._get_power(x, y, 3)
                if power > max_power:
                    max_power = power
                    result = f"{x},{y}"

        print("Part 1:", result)

    def part2(self):
        result = None
        max_power = 0

        for size in range(1, 301):
            for x in range(300 - size):
                for y in range(300 - size):
                    power = self._get_power(x, y, size)
                    if power > max_power:
                        max_power = power
                        result = f"{x},{y},{size}"

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2018D11("2018/11.txt")
    # code.part1()
    code.part2()
