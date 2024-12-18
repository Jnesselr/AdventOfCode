from tqdm import tqdm

from aoc.util.coordinate import Coordinate, CoordinateSystem
from aoc.util.grid import Grid
from aoc.util.inputs import Input


class Y2024D18(object):
    grid_end = 70

    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self._coordinates: list[Coordinate] = [
            Coordinate(int(a), int(b), CoordinateSystem.X_RIGHT_Y_DOWN)
            for a, b in [x.split(',') for x in lines]
        ]

    def part1(self):
        grid: Grid[str] = Grid(self.grid_end + 1, self.grid_end + 1)
        for coordinate in self._coordinates[:1024]:
            grid[coordinate] = '#'

        grid.fill_empty('.')

        path = grid.find_path(
            Coordinate(0, 0, CoordinateSystem.X_RIGHT_Y_DOWN),
            Coordinate(self.grid_end, self.grid_end, CoordinateSystem.X_RIGHT_Y_DOWN),
            '.'
        )
        result = len(path) - 1  # steps required, not coordinates

        print("Part 1:", result)

    def part2(self):
        grid: Grid[str] = Grid(self.grid_end + 1, self.grid_end + 1)
        grid.fill('.')

        last_path: set[Coordinate] = set()

        result = "unknown"

        for coordinate in self._coordinates:
            grid[coordinate] = '#'

            if last_path and coordinate not in last_path:
                continue  # The last good path was not interrupted, so the new coordinate can't block us

            path = grid.find_path(
                Coordinate(0, 0, CoordinateSystem.X_RIGHT_Y_DOWN),
                Coordinate(self.grid_end, self.grid_end, CoordinateSystem.X_RIGHT_Y_DOWN),
                '.'
            )
            if path is None:
                result = f"{coordinate.x},{coordinate.y}"
                break

            last_path = set(path)



        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2024D18("2024/18.txt")
    code.part1()
    code.part2()
