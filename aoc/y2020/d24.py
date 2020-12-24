from typing import Set

from aoc.util.coordinate import Coordinate
from aoc.util.grid import InfiniteGrid
from aoc.util.inputs import Input


class Y2020D24(object):
    def __init__(self, file_name):
        self.instructions = Input(file_name).lines()
        self.grid: InfiniteGrid[bool] = InfiniteGrid[bool]()

        reference_coordinate = Coordinate(0, 0)

        for instruction in self.instructions:
            coordinate = reference_coordinate
            index = 0
            while index < len(instruction):
                if instruction[index] == 'n':
                    if instruction[index + 1] == 'w':
                        coordinate = coordinate.left().up()
                    elif instruction[index + 1] == 'e':
                        coordinate = coordinate.up()
                    index += 2
                elif instruction[index] == 's':
                    if instruction[index + 1] == 'w':
                        coordinate = coordinate.down()
                    elif instruction[index + 1] == 'e':
                        coordinate = coordinate.right().down()
                    index += 2
                elif instruction[index] == 'w':
                    coordinate = coordinate.left()
                    index += 1
                elif instruction[index] == 'e':
                    coordinate = coordinate.right()
                    index += 1

            if coordinate in self.grid:
                self.grid[coordinate] = not self.grid[coordinate]
            else:
                self.grid[coordinate] = True

    def part1(self):
        result = len(self.grid.find(True))

        print("Part 1:", result)

    def part2(self):
        grid = self.grid
        for i in range(100):
            grid = self._mutate(grid)
            print(i, len(grid.find(True)))

        result = len(grid.find(True))

        print("Part 2:", result)

    @staticmethod
    def _neighbors(coordinate: Coordinate) -> Set[Coordinate]:
        return {
            coordinate.left().up(),
            coordinate.up(),
            coordinate.down(),
            coordinate.right().down(),
            coordinate.left(),
            coordinate.right()
        }

    def _mutate(self, grid: InfiniteGrid[bool]) -> InfiniteGrid[bool]:
        new_grid = grid.copy()

        black_tiles = set(grid.find(True))
        to_check_tiles = set(neighbor for coordinate in black_tiles for neighbor in self._neighbors(coordinate))
        to_check_tiles = to_check_tiles.union(black_tiles)

        for coordinate in to_check_tiles:
            tile_is_black = bool(grid[coordinate])  # None or False are both False so cast to bool

            black_neighbor_tiles = sum(1 for neighbor in self._neighbors(coordinate) if bool(grid[neighbor]))

            if tile_is_black and (black_neighbor_tiles == 0 or black_neighbor_tiles > 2):
                new_grid[coordinate] = False
            elif not tile_is_black and black_neighbor_tiles == 2:
                new_grid[coordinate] = True

        return new_grid



if __name__ == '__main__':
    code = Y2020D24("2020/24.txt")
    code.part1()
    code.part2()
