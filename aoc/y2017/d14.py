from queue import Queue

from aoc.util.grid import Grid
from aoc.util.inputs import Input
from aoc.y2017.knot_hash import KnotHash


class Y2017D14(object):
    def __init__(self, file_name):
        self.key_string = Input(file_name).line()

        grid: Grid[str] = Grid[str](128, 128)

        for row in range(128):
            bin_output = KnotHash(f"{self.key_string}-{row}").bin
            for col in range(128):
                grid[col, row] = "#" if bin_output[col] == '1' else '.'

        self.coordinates = grid.find('#')

    def part1(self):
        result = len(self.coordinates)

        print("Part 1:", result)

    def part2(self):
        groups = []
        coordinates = set(self.coordinates)

        while len(coordinates) > 0:
            coordinate = coordinates.pop()
            current_group = {coordinate}
            queue = Queue()
            queue.put(coordinate)

            while not queue.empty():
                item = queue.get()
                current_group.add(item)
                for neighbor in item.neighbors():
                    if neighbor in coordinates:
                        coordinates.remove(neighbor)
                        queue.put(neighbor)
            groups.append(current_group)

        result = len(groups)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2017D14("2017/14.txt")
    code.part1()
    code.part2()
