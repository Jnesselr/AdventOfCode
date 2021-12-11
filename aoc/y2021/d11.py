from queue import Queue

from aoc.util.coordinate import Coordinate
from aoc.util.grid import InfiniteGrid
from aoc.util.inputs import Input


class Y2021D11(object):
    def __init__(self, file_name):
        self._grid = Input(file_name).grid().map(lambda x: int(x))

    def part1(self):
        result = 0

        grid = self._grid.copy()
        for _ in range(100):
            result += self._step(grid)

        print("Part 1:", result)

    def part2(self):
        grid = self._grid.copy()
        step = 0
        while True:
            step += 1
            flash_count = self._step(grid)
            if flash_count == 100:
                result = step
                break

        print("Part 2:", result)

    @staticmethod
    def _step(grid: InfiniteGrid[int]) -> int:
        result = 0

        for row in range(10):
            for col in range(10):
                grid[col, row] = grid[col, row] + 1

        should_flash = grid.find(lambda value: value > 9)
        already_flashed = set()
        queue: Queue = Queue()
        while should_flash:
            queue.put(should_flash.pop())

        while not queue.empty():
            coordinate: Coordinate = queue.get()
            if coordinate in already_flashed:
                continue

            already_flashed.add(coordinate)
            grid[coordinate] = 0
            result += 1

            neighbors = coordinate.neighbors8()

            for neighbor in neighbors:
                if neighbor not in grid:
                    continue

                if neighbor in already_flashed:
                    continue

                grid[neighbor] += 1

                if grid[neighbor] > 9:
                    queue.put(neighbor)

        return result


if __name__ == '__main__':
    code = Y2021D11("2021/11.txt")
    code.part1()
    code.part2()
