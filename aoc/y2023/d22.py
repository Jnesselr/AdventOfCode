import re
from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property
from itertools import permutations
from queue import Queue
from typing import Self

from aoc.util.inputs import Input
from aoc.util.queue import PriorityQueue


@dataclass(frozen=True)
class Coordinate3D:
    x: int
    y: int
    z: int

    @property
    def up(self) -> Self:
        return Coordinate3D(self.x, self.y, self.z + 1)


@dataclass(frozen=True)
class Block:
    start_x: int
    start_y: int
    start_z: int
    end_x: int
    end_y: int
    end_z: int

    @cached_property
    def coordinates(self) -> set[Coordinate3D]:
        if self.start_y == self.end_y and self.start_z == self.end_z:  # x
            return set(Coordinate3D(x, self.start_y, self.start_z) for x in range(self.start_x, self.end_x + 1))

        if self.start_x == self.end_x and self.start_z == self.end_z:  # y
            return set(Coordinate3D(self.start_x, y, self.start_z) for y in range(self.start_y, self.end_y + 1))

        if self.start_x == self.end_x and self.start_y == self.end_y:  # z
            return set(Coordinate3D(self.start_x, self.start_y, z) for z in range(self.start_z, self.end_z + 1))

    def intersects(self, other: 'Block') -> bool:
        return not self.coordinates.isdisjoint(other.coordinates)  # disjoint coordinates don't intersect

    @property
    def can_drop(self) -> bool:
        return self.start_z != 1 and self.end_z != 1

    @property
    def dropped(self) -> Self:
        if not self.can_drop:
            return self

        return Block(
            start_x=self.start_x,
            start_y=self.start_y,
            start_z=self.start_z - 1,
            end_x=self.end_x,
            end_y=self.end_y,
            end_z=self.end_z - 1,
        )

    def __repr__(self):
        return f"{self.start_x},{self.start_y},{self.start_z}~{self.end_x},{self.end_y},{self.end_z}"


class Y2023D22(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()

        q: PriorityQueue[Block] = PriorityQueue()

        line_re = re.compile(r'(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)')
        for line in lines:
            match = line_re.match(line)
            block = Block(
                start_x=int(match.group(1)),
                start_y=int(match.group(2)),
                start_z=int(match.group(3)),
                end_x=int(match.group(4)),
                end_y=int(match.group(5)),
                end_z=int(match.group(6)),
            )
            q.push(block, min(block.start_z, block.end_z))

        self.blocks: set[Block] = set()
        filled_coordinates: set[Coordinate3D] = set()
        while not q.empty:
            block: Block = q.pop()

            # Drop until you either hit the ground or something else
            while block.can_drop:
                dropped = block.dropped
                if dropped.coordinates.isdisjoint(filled_coordinates):
                    block = dropped
                else:
                    break

            self.blocks.add(block)
            filled_coordinates.update(block.coordinates)

        self.above: defaultdict[Block, set[Block]] = defaultdict(lambda: set())
        self.below: defaultdict[Block, set[Block]] = defaultdict(lambda: set())

        for a, b in permutations(self.blocks, 2):
            if a.can_drop and a.dropped.intersects(b):
                self.above[b].add(a)
                self.below[a].add(b)

        self.cannot_disintegrate: set[Block] = set()
        for a, b in permutations(self.blocks, 2):
            a_depends_on = self.below[a]
            if len(a_depends_on) == 1 and b in a_depends_on:  # b MUST continue to exist for a not to fall
                self.cannot_disintegrate.add(b)

    def part1(self):
        result = len(self.blocks) - len(self.cannot_disintegrate)

        print("Part 1:", result)

    def part2(self):
        result = 0
        for block in self.cannot_disintegrate:
            q: Queue = Queue()
            q.put(block)
            would_fall: set[Block] = {block}
            while not q.empty():
                me: Block = q.get()
                for test in self.above[me]:
                    if all(b in would_fall for b in self.below[test]):
                        q.put(test)
                        would_fall.add(test)

            result += len(would_fall) - 1  # - 1 because we counted block in the beginning to make the algorithm work

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2023D22("2023/22.txt")
    code.part1()
    code.part2()
