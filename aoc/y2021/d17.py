import re
from queue import Queue
from typing import Optional, Set

from aoc.util.coordinate import BoundingBox, Coordinate
from aoc.util.grid import InfiniteGrid
from aoc.util.inputs import Input


class FiringAttempt(object):
    def __init__(self, x_velocity: int, y_velocity: int):
        self._x = 0
        self._y = 0
        self._x_velocity = x_velocity
        self._y_velocity = y_velocity
        self._max_y = 0

    @property
    def coordinate(self) -> Coordinate:
        return Coordinate(self._x, self._y)

    @property
    def max_y(self) -> int:
        return self._max_y

    def step(self):
        self._x += self._x_velocity
        self._y += self._y_velocity
        self._max_y = max(self._max_y, self._y)

        if self._x_velocity > 0:
            self._x_velocity -= 1
        elif self._x_velocity < 0:
            self._x_velocity += 1

        self._y_velocity -= 1

    def step_until(self, bounding_box: BoundingBox) -> Optional[Coordinate]:
        while self._y >= bounding_box.min_y:
            if self.coordinate in bounding_box:
                return self.coordinate
            self.step()

        return None


class Y2021D17(object):
    def __init__(self, file_name):
        line = Input(file_name).line()

        target_regex = re.compile(r'target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)')
        match = target_regex.match(line)
        box = BoundingBox()
        box = box.expand_x(int(match.group(1)))
        box = box.expand_x(int(match.group(2)))
        box = box.expand_y(int(match.group(3)))
        box = box.expand_y(int(match.group(4)))
        self.target = box

        grid: InfiniteGrid[str] = InfiniteGrid[str]()

        start_x = 1
        attempt = FiringAttempt(start_x, 0)
        while attempt.step_until(self.target) is None:
            start_x += 1
            attempt = FiringAttempt(start_x, 0)

        starting_coordinate = Coordinate(start_x, 0)
        queue: Queue = Queue()
        queue.put(starting_coordinate)
        seen: Set[Coordinate] = set()
        seen.add(starting_coordinate)

        max_y = 0

        while not queue.empty():
            item: Coordinate = queue.get()
            attempt = FiringAttempt(item.x, item.y)
            end = attempt.step_until(self.target)
            if end is not None:
                max_y = max(max_y, attempt.max_y)
                grid[item] = '*'
                for dx in range(-5, 20):
                    for dy in range(-20, 20):
                        neighbor = Coordinate(item.x + dx, item.y + dy)
                        if neighbor in seen:
                            continue

                        queue.put(neighbor)
                        seen.add(neighbor)

        for x in range(self.target.min_x, self.target.max_x + 1):
            for y in range(self.target.min_y, self.target.max_y + 1):
                grid[Coordinate(x, y)] = '#'

        grid[Coordinate(0, 0)] = '!'
        # grid.to_grid().print(not_found='.')

        self.max_y = max_y
        self.hitting_velocity_count = len(grid.find(lambda _: _ in '*#'))

    def part1(self):
        result = self.max_y

        print("Part 1:", result)

    def part2(self):
        result = self.hitting_velocity_count

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2021D17("2021/17.txt")
    code.part1()
    code.part2()
