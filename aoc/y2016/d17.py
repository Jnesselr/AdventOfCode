from __future__ import  annotations

import hashlib
from dataclasses import dataclass
from queue import Queue
from typing import Set

from aoc.util.coordinate import Coordinate, CoordinateSystem
from aoc.util.inputs import Input
from aoc.util.queue import PriorityQueue


@dataclass(frozen=True)
class SearchAttempt(object):
    steps: str
    coordinate: Coordinate

    @staticmethod
    def _is_open(value: str):
        return value in 'bcdef'

    def open_paths(self, passcode: str) -> Set[SearchAttempt]:
        md5_hash = hashlib.md5(f'{passcode}{self.steps}'.encode()).hexdigest()

        result = set()
        if self.coordinate.y > 0 and self._is_open(md5_hash[0]):
            result.add(SearchAttempt(self.steps + 'U', self.coordinate.up()))

        if self.coordinate.y < 3 and self._is_open(md5_hash[1]):
            result.add(SearchAttempt(self.steps + 'D', self.coordinate.down()))

        if self.coordinate.x > 0 and self._is_open(md5_hash[2]):
            result.add(SearchAttempt(self.steps + 'L', self.coordinate.left()))

        if self.coordinate.x < 3 and self._is_open(md5_hash[3]):
            result.add(SearchAttempt(self.steps + 'R', self.coordinate.right()))

        return result


class Y2016D17(object):
    def __init__(self, file_name):
        self.passcode = Input(file_name).line()

    def part1(self):
        queue: PriorityQueue[SearchAttempt] = PriorityQueue[SearchAttempt]()
        queue.push(SearchAttempt(steps="", coordinate=Coordinate(0, 0, system=CoordinateSystem.X_RIGHT_Y_DOWN)), 0)

        result = None

        while not queue.empty:
            item: SearchAttempt = queue.pop()

            if item.coordinate.x == 3 and item.coordinate.y == 3:
                result = item.steps
                break

            for next_attempt in item.open_paths(self.passcode):
                queue.push(next_attempt, len(next_attempt.steps))

        print("Part 1:", result)

    def part2(self):
        queue = Queue()
        queue.put(SearchAttempt(steps="", coordinate=Coordinate(0, 0, system=CoordinateSystem.X_RIGHT_Y_DOWN)))

        result = ""

        while not queue.empty():
            item: SearchAttempt = queue.get()

            if item.coordinate.x == 3 and item.coordinate.y == 3:
                if len(result) < len(item.steps):
                    result = item.steps
                continue

            for next_attempt in item.open_paths(self.passcode):
                queue.put(next_attempt)

        print("Part 2:", len(result))


if __name__ == '__main__':
    code = Y2016D17("2016/17.txt")
    code.part1()
    code.part2()
