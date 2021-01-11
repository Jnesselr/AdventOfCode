from aoc.util.coordinate import Coordinate
from aoc.util.grid import InfiniteGrid
from aoc.util.inputs import Input


class Y2015D3(object):
    def __init__(self, file_name):
        self.path = Input(file_name).line()

    def part1(self):
        grid = InfiniteGrid[bool]()

        santa = Coordinate(0, 0)
        grid[santa] = True
        for character in self.path:
            santa = santa.move(character)
            grid[santa] = True

        result = len(grid.find(True))

        print("Part 1:", result)

    def part2(self):
        grid = InfiniteGrid[bool]()

        santa = Coordinate(0, 0)
        robot_santa = santa
        grid[santa] = True
        for index, character in enumerate(self.path):
            if index % 2 == 0:
                santa = santa.move(character)
                grid[santa] = True
            else:
                robot_santa = robot_santa.move(character)
                grid[robot_santa] = True

        result = len(grid.find(True))

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2015D3("2015/3.txt")
    code.part1()
    code.part2()
