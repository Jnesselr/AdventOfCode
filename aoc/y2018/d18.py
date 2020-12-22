import hashlib

from aoc.util.grid import Grid
from aoc.util.inputs import Input


class Y2018D18(object):
    def __init__(self, file_name):
        self.initial_grid = Input(file_name).grid()

    def part1(self):
        grid = self.initial_grid.copy()

        for i in range(10):
            grid = self._mutate(grid)

        wooded = len(grid.find('|'))
        lumberyards = len(grid.find('#'))
        result = wooded * lumberyards

        print("Part 1:", result)

    def part2(self):
        grid = self.initial_grid.copy()
        grid_lookup = {}
        minute_lookup = {}

        my_hash = self._hash(grid)
        minute = 0
        while my_hash not in grid_lookup:
            grid_lookup[my_hash] = grid
            minute_lookup[my_hash] = minute

            grid = self._mutate(grid)
            my_hash = self._hash(grid)
            minute += 1

        wanted = 1000000000
        remaining = (wanted - minute) % (minute - minute_lookup[my_hash])

        for _ in range(remaining):
            grid = self._mutate(grid)

        wooded = len(grid.find('|'))
        lumberyards = len(grid.find('#'))
        result = wooded * lumberyards

        print("Part 2:", result)

    @staticmethod
    def _hash(grid: Grid[str]):
        coordinates = sorted(list(grid))

        md5_func = hashlib.md5()
        for coordinate in coordinates:
            md5_func.update(str(coordinate).encode())
            md5_func.update(grid[coordinate].encode())

        return md5_func.hexdigest()

    @staticmethod
    def _mutate(grid: Grid[str]) -> Grid[str]:
        result = Grid[str](grid.width, grid.height)

        for coordinate, acre in grid.items():
            tree_count = 0
            lumberyard_count = 0
            for neighbor in coordinate.neighbors8():
                if grid[neighbor] == '|':
                    tree_count += 1
                elif grid[neighbor] == '#':
                    lumberyard_count += 1

            if acre == '.' and tree_count >= 3:
                result[coordinate] = '|'
            elif acre == '|' and lumberyard_count >= 3:
                result[coordinate] = '#'
            elif acre == '#' and (lumberyard_count < 1 or tree_count < 1):
                result[coordinate] = '.'
            else:
                result[coordinate] = acre

        return result


if __name__ == '__main__':
    code = Y2018D18("2018/18.txt")
    code.part1()
    code.part2()
