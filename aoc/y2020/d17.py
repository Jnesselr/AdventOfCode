from aoc.util.grid import Grid
from aoc.util.inputs import Input


class Y2020D17(object):
    def __init__(self, file_name):
        self.base_grid = Grid.from_str(Input(file_name).lines())

    def part1(self):
        grid = set()

        for coordinate, item in self.base_grid.items():
            if item == '#':
                grid.add((coordinate.x, coordinate.y, 0))
        
        for i in range(6):
            grid = self._mutate_3(grid)
        
        result = len(grid)

        print("Part 1:", result)

    def part2(self):
        grid = set()

        for coordinate, item in self.base_grid.items():
            if item == '#':
                grid.add((coordinate.x, coordinate.y, 0, 0))

        for i in range(6):
            grid = self._mutate_4(grid)

        result = len(grid)

        print("Part 2:", result)

    def _mutate_3(self, grid):
        result = set()
        min_x = min_y = min_z = 2**24
        max_x = max_y = max_z = -2**24
        
        for coordinate in grid:
            min_x = min(min_x, coordinate[0])
            min_y = min(min_y, coordinate[1])
            min_z = min(min_z, coordinate[2])
            max_x = max(max_x, coordinate[0])
            max_y = max(max_y, coordinate[1])
            max_z = max(max_z, coordinate[2])
            
        for x in range(min_x - 1, max_x + 2):
            for y in range(min_y - 1, max_y + 2):
                for z in range(min_z - 1, max_z + 2):
                    coordinate = (x, y, z)
                    neighbor_count = self._neighbor_count_3(grid, x, y, z)

                    if coordinate in grid and 2 <= neighbor_count <= 3:
                        result.add(coordinate)
                    if coordinate not in grid and neighbor_count == 3:
                        result.add(coordinate)
        
        return result

    def _neighbor_count_3(self, grid, x, y, z):
        result = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                for k in range(-1, 2):
                    if i == j == k == 0:
                        continue
                    coordinate = (x + i, y + j, z + k)
                    if coordinate in grid:
                        result += 1

        return result

    def _mutate_4(self, grid):
        result = set()
        min_x = min_y = min_z = min_w = 2 ** 24
        max_x = max_y = max_z = max_w = -2 ** 24

        for coordinate in grid:
            min_x = min(min_x, coordinate[0])
            min_y = min(min_y, coordinate[1])
            min_z = min(min_z, coordinate[2])
            min_w = min(min_w, coordinate[3])
            max_x = max(max_x, coordinate[0])
            max_y = max(max_y, coordinate[1])
            max_z = max(max_z, coordinate[2])
            max_w = max(max_w, coordinate[3])

        for x in range(min_x - 1, max_x + 2):
            for y in range(min_y - 1, max_y + 2):
                for z in range(min_z - 1, max_z + 2):
                    for w in range(min_w - 1, max_w + 2):
                        coordinate = (x, y, z, w)
                        neighbor_count = self._neighbor_count_4(grid, x, y, z, w)

                        if coordinate in grid and 2 <= neighbor_count <= 3:
                            result.add(coordinate)
                        if coordinate not in grid and neighbor_count == 3:
                            result.add(coordinate)

        return result

    def _neighbor_count_4(self, grid, x, y, z, w):
        result = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        if i == j == k == l == 0:
                            continue
                        coordinate = (x + i, y + j, z + k, w + l)
                        if coordinate in grid:
                            result += 1

        return result



if __name__ == '__main__':
    code = Y2020D17("2020/17.txt")
    code.part1()
    code.part2()
