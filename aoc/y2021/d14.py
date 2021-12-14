from collections import Counter
from typing import Dict, Tuple

from aoc.util.inputs import Input


class Polymerization(object):
    def __init__(self, initial: str, pairs: Dict[str, str]):
        self._initial = initial
        self._pairs = pairs
        self._memory: Dict[Tuple[str, int], Counter[str, int]] = {}

    def find(self, max_depth: int) -> int:
        counter = Counter()

        for index in range(len(self._initial) - 1):
            pair = self._initial[index:index + 2]
            counter += Counter(self.morph(pair, max_depth))
            if index > 0:
                counter[pair[0]] -= 1  # Remove overlap

        most_common = counter.most_common()

        return most_common[0][1] - most_common[-1][1]

    def morph(self, pair: str, current_depth: int) -> Counter[str, int]:
        t: Tuple[str, int] = (pair, current_depth)

        if t in self._memory:
            return self._memory[t]

        if current_depth == 0:
            if pair[0] == pair[1]:
                self._memory[t] = Counter({pair[0]: 2})
            else:
                self._memory[t] = Counter({pair[0]: 1, pair[1]: 1})
        else:
            next_poly = self._pairs[pair]
            left = pair[0] + next_poly
            right = next_poly + pair[1]
            counter: Counter[str, int] = self.morph(left, current_depth - 1) + self.morph(right, current_depth - 1)
            counter[next_poly] -= 1  # Remove overlap
            self._memory[t] = counter

        return self._memory[t]


class Y2021D14(object):
    def __init__(self, file_name):
        start, pairs = Input(file_name).grouped()

        pairs_map: Dict[str, str] = {}
        pair: str
        for pair in pairs:
            _from, _to = pair.split(' -> ')
            pairs_map[_from] = _to

        self._poly = Polymerization(start[0], pairs_map)

    def part1(self):
        print("Part 1:", self._poly.find(10))

    def part2(self):
        print("Part 2:", self._poly.find(40))


if __name__ == '__main__':
    code = Y2021D14("2021/14.txt")
    code.part1()
    code.part2()
