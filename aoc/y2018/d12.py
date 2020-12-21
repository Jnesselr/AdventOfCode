from __future__ import annotations
import re
from dataclasses import dataclass, field
from typing import Dict

from aoc.util.inputs import Input


@dataclass(frozen=True)
class Pots(object):
    state: str
    transforms: Dict[str, str] = field(compare=False, repr=False)
    offset: int = field(compare=False, default=0)

    def next(self) -> Pots:
        new_offset = self.offset
        state = self.state
        new_state = ""

        while state[:4] != '....':
            state = '.' + state
            new_offset -= 1

        while state[-4:] != '....':
            state = state + '.'

        for i in range(0, len(state) - 4):
            subsection = state[i:i + 5]
            if subsection in self.transforms:
                new_state += self.transforms[subsection]
            else:
                new_state += '.'

        new_offset += 2  # Cut off the first 2 characters, essentially

        return Pots(new_state, self.transforms, new_offset)

    def value(self) -> int:
        return sum(index + self.offset for index, value in enumerate(self.state) if value == '#')


class Y2018D12(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        initial_state = re.search(r"initial state: (.*)", lines[0]).group(1)
        transforms = dict(tuple(line.split(' => ')) for line in lines[2:])
        self.initial_pots = Pots(initial_state, transforms)

    def part1(self):
        pots = self.initial_pots
        for i in range(20):
            pots = pots.next()

        result = pots.value()

        print("Part 1:", result)

    def part2(self):
        seen_pots = {}
        pots = self.initial_pots
        generation = 0
        while pots not in seen_pots:
            seen_pots[pots] = pots
            pots = pots.next()
            generation += 1

        latest_value = pots.value()
        previous_value = seen_pots[pots].value()
        value_change = latest_value - previous_value
        result = (50000000000 - generation) * value_change + latest_value

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2018D12("2018/12.txt")
    code.part1()
    code.part2()
