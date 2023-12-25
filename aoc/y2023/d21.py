from typing import Optional

from aoc.util.coordinate import Coordinate, CoordinateSystem
from aoc.util.inputs import Input


class Y2023D21(object):
    def __init__(self, file_name):
        self.grid = Input(file_name).grid()

        self._steps: dict[int, set[Coordinate]] = {
            0: set(self.grid.find('S'))
        }

        self._rocks = set(self.grid.find('#'))

    def part1(self):
        self.step(64)
        result = len(self._steps[64])

        print("Part 1:", result)

    def part2(self):
        # 26501365 is 65 + 131 * 202300 and 131 is our grid size
        # Expansion is quadratic. Find f(n), f(n + 1 * 131), and f(n + 2 * 131)
        # Key thing to notice is our actual input is a diamond shape with nothing on the rows and columns. More or less
        # guarantees a quadratic.
        x0 = 0
        x1 = 1
        x2 = 2

        self.step(65 * x2 + 31)  # Step until f(n + 2 * 31)

        y0 = 3744 # len(self._steps[x0])
        y1 = 33417 # len(self._steps[x1])
        y2 = 92680 # len(self._steps[x2])

        x0_sq = pow(x0, 2)
        x1_sq = pow(x1, 2)
        x2_sq = pow(x2, 2)
        a = ((y2 - y0) * (x1 - x0) - (y1 - y0) * (x2 - x0)) // \
            ((x2_sq - x0_sq) * (x1 - x0) - (x1_sq - x0_sq) * (x2 - x0))
        b = (y1 - y0 - a * (x1_sq - x0_sq)) // (x1 - x0)
        c = y0 - a * x0_sq + b * x0

        x = 202300
        result = a * pow(x, 2) + b * x + c

        print("Part 2:", result)

        """
        Here's the math I don't want to think about again:
        Start with:
        y0 = a * x0^2 + b * x0 + c
        y1 = a * x1^2 + b * x1 + c
        y2 = a * x2^2 + b * x2 + c
        
        Subtract y1 - y0 and y2 - y0 to get rid of the C term
        y1 - y0 = a * x1^2 + b * x1 + c - (a * x0^2 + b * x0 + c)
        y2 - y0 = a * x2^2 + b * x2 + c - (a * x0^2 + b * x0 + c)
        
        Simplified:
        y1 - y0 = a(x1^2 - x0^2) + b(x1 - x0)
        y2 - y0 = a(x2^2 - x0^2) + b(x2 - x0)
        
        Multiplying (y1 - y0) by (x2 - x0) and (y2 - y0) by (x1 - x0) makes the b multiple in both equations have the same term:
        (y1 - y0)(x2 - x0) = a(x1^2 - x0^2)(x2 - x0) + b(x1 - x0)(x2 - x0)
        (y2 - y0)(x1 - x0) = a(x2^2 - x0^2)(x1 - x0) + b(x2 - x0)(x1 - x0)
        
        Isolate a by subtracting the first equation from the second:
        (y2 - y0)(x1 - x0) - (y1 - y0)(x2 - x0) = a((x2^2 - x0^2)(x1 - x0) - (x1^2 - x0^2)(x2 - x0))
        a = ((y2 - y0)(x1 - x0) - (y1 - y0)(x2 - x0)) / ((x2^2 - x0^2)(x1 - x0) - (x1^2 - x0^2)(x2 - x0))
        
        Those are all constant inputs on the right. Next we find b by isolating it in one of the equations above:
        y1 - y0 = a(x1^2 - x0^2) + b(x1 - x0)
        b = (y1 - y0 - a(x1^2 - x0^2)) / (x1 - x0)
        
        Finally the same with c:
        y0 = a * x0^2 + b * x0 + c
        c = y0 - a * x0^2 + b * x0
        """

    def step(self, until: Optional[int] = None):
        last_step = max(self._steps.keys())
        if until is not None and last_step >= until:
            return  # Nothing to do

        while True:
            last_possibilities = self._steps[last_step]

            new_possibilities = set()
            for step in last_possibilities:
                for neighbor in step.neighbors():
                    check_neighbor = neighbor
                    if neighbor.x < 0 or neighbor.y < 0 or neighbor.x >= self.grid.width or neighbor.y >= self.grid.height:
                        check_neighbor = Coordinate(
                            x=neighbor.x % self.grid.width,
                            y=neighbor.y % self.grid.height,
                            system=CoordinateSystem.X_RIGHT_Y_DOWN
                        )  # TODO This algorithm could be sped up a lot of we didn't keep track of every instance but kept up with how many copies at each coordinate we have
                    if check_neighbor in self._rocks:
                        continue
                    new_possibilities.add(neighbor)

            last_step += 1
            self._steps[last_step] = new_possibilities
            if until is not None and last_step >= until:
                return  # We're all done counting


if __name__ == '__main__':
    code = Y2023D21("2023/21.txt")
    code.part1()
    code.part2()
