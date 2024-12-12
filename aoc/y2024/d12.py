from dataclasses import dataclass
from queue import Queue

from aoc.util.coordinate import Coordinate, CoordinateSystem
from aoc.util.inputs import Input


@dataclass(frozen=True)
class Fencing:
    first: Coordinate
    second: Coordinate

    def __post_init__(self):
        # We try to force first to be above and to the left of second
        swap = False
        if self.first.up() == self.second:
            swap = True
        elif self.first.left() == self.second:
            swap = True
        elif self.first.down() == self.second:
            pass  # This is fine
        elif self.first.right() == self.second:
            pass  # This is fine
        else:  # Anything else is not fine
            raise Exception(f"{self.first} must be a neighbor of {self.second}")

        if swap:
            temp = self.second
            object.__setattr__(self, 'second', self.first)
            object.__setattr__(self, 'first', temp)

    @property
    def left_ish(self) -> 'Fencing':
        if self.first.down() == self.second:
            # second is below first, left is their actual lefts
            return Fencing(
                self.first.left(),
                self.second.left()
            )
        elif self.first.right() == self.second:
            # second is to the right of first, left is up
            return Fencing(
                self.first.up(),
                self.second.up()
            )
        else:
            raise Exception("Should never get here")


Region = frozenset[Coordinate]


class Y2024D12(object):
    def __init__(self, file_name):
        self._grid = Input(file_name).grid()

        all_coordinates: set[Coordinate] = set(self._grid.keys())
        to_test: set[Coordinate] = set(all_coordinates)
        self._region_map: dict[Region, set[Fencing]] = {}

        while len(to_test) > 0:
            starting_coordinate = to_test.pop()
            region_value = self._grid[starting_coordinate]
            this_region: set[Coordinate] = {starting_coordinate}
            q: Queue = Queue()
            q.put(starting_coordinate)
            fencing: set[Fencing] = set()

            while not q.empty():
                coordinate = q.get()
                for neighbor in coordinate.neighbors():
                    if self._grid[neighbor] != region_value:
                        # Add fencing regardless of if we've seen it before, the set will sort out duplicates
                        fencing.add(Fencing(
                            first=coordinate,
                            second=neighbor
                        ))
                        continue  # Not part of our region

                    if neighbor in this_region:
                        continue  # Already seen it

                    this_region.add(neighbor)
                    to_test.remove(neighbor)
                    q.put(neighbor)

            self._region_map[frozenset(this_region)] = fencing

    def part1(self):
        result = 0

        for region, fencing in self._region_map.items():
            perimeter = len(fencing)
            area = len(region)

            result += perimeter * area

        print("Part 1:", result)

    def part2(self):
        result = 0

        for region, fencing in self._region_map.items():
            simple_fencing: set[Fencing] = set(fencing)
            for fence in fencing:
                while (left_ish := fence.left_ish) in fencing:
                    if self._grid[fence.first] != self._grid[left_ish.first] and \
                            self._grid[fence.second] != self._grid[left_ish.second]:
                        # This would make a cross in the fence. How bad could the Möbius Fencing Company have been, anyway?
                        break
                    if fence in simple_fencing:
                        simple_fencing.remove(fence)
                    fence = left_ish

            perimeter = len(simple_fencing)
            area = len(region)

            result += perimeter * area

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2024D12("2024/12.txt")
    code.part1()
    code.part2()
