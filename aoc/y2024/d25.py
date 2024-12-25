from aoc.util.grid import Grid
from aoc.util.inputs import Input


class Y2024D25(object):
    def __init__(self, file_name):
        groups = Input(file_name).grouped()
        grids = [Grid.from_str(lines) for lines in groups]

        self._locks = []
        self._keys = []

        for grid in grids:
            is_lock = grid[0, 0] == '#'

            combo = []
            for x in range(grid.width):
                height_with_body = sum(1 for y in range(grid.height) if grid[x, y] == '#')
                combo.append(height_with_body - 1)

            if is_lock:
                self._locks.append(tuple(combo))
            else:
                self._keys.append(tuple(combo))

    def part1(self):
        result = 0
        for lock in self._locks:
            for key in self._keys:
                match = [l+k for l, k in zip(lock, key)]
                if not all(m <= 5 for m in match):
                    continue
                print(lock, key)
                result += 1

        print(result)

        print("Part 1:", result)


if __name__ == '__main__':
    code = Y2024D25("2024/25.txt")
    code.part1()
