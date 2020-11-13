from aoc.util.grid import Grid
from aoc.util.intcode import Intcode


class Y2019D17(object):
    def __init__(self, file_name):
        self.computer = Intcode(file_name)


    def part1(self):
        self.computer.reset()
        self.computer.run()
        map_string = self.computer.output_str()
        grid = Grid.from_str(map_string)

        result = 0
        scaffolding = grid.find('#')

        for scaffold in scaffolding:
            intersecting = all(grid[neighbor] == '#' for neighbor in scaffold.neighbors())

            if intersecting:
                result += scaffold.x * scaffold.y

        print("Part 1:", result)

    def part2(self):
        self.computer.reset()
        self.computer.ram[0] = 2
        self.computer.run()

        self.computer.output_str()
        self.computer.input_str("B,C,B,C,A,B,C,A,B,A\n")
        self.computer.output_str()
        self.computer.input_str("R,6,L,8,L,10,R,6\n")
        self.computer.output_str()
        self.computer.input_str("R,6,L,6,L,10\n")
        self.computer.output_str()
        self.computer.input_str("L,8,L,6,L,10,L,6\n")
        self.computer.output_str()
        self.computer.input_str("n\n")
        map_string = self.computer.output_str()
        grid = Grid.from_str(map_string)
        result = self.computer.output()

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2019D17("2019/17.txt")
    code.part1()
    code.part2()
