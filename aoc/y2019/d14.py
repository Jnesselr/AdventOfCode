from dataclasses import dataclass
from typing import List

from aoc.util.inputs import Input


@dataclass(frozen=True)
class Element(object):
    name: str
    amount: int

    @classmethod
    def from_string(cls, string):
        amount, name = string.split(' ')
        return Element(name=name, amount=int(amount))


@dataclass(frozen=True)
class Reaction(object):
    makes: Element
    needed: List[Element]


class Y2019D14(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.reactions = {}

        for line in lines:
            needed_str, makes_str = line.split(' => ')
            needed = []

            for element in needed_str.split(', '):
                needed.append(Element.from_string(element))

            makes = Element.from_string(makes_str)
            self.reactions[makes.name] = Reaction(makes, needed)

    def part1(self):
        result = self._get_ore_cost(1)

        print("Part 1:", result)

    def part2(self):
        max_ore = 1000000000000
        start = 0
        end = max_ore

        while start + 1 < end:
            current = (start + end) // 2
            ore_needed = self._get_ore_cost(current)

            if ore_needed > max_ore:
                end = current
            elif ore_needed < max_ore:
                start = current

        result = start

        print("Part 2:", result)

    def _get_ore_cost(self, fuel) -> int:
        needed = {'FUEL': fuel}
        have = {}
        ore = 0

        while needed:
            source_name, source_amount = needed.popitem()

            if source_name == 'ORE':
                ore += source_amount
                continue

            reaction = self.reactions[source_name]

            multiplier = ((source_amount - 1) // reaction.makes.amount) + 1
            produces = multiplier * reaction.makes.amount
            have[source_name] = have.setdefault(source_name, 0) + produces - source_amount

            for element in reaction.needed:
                element_needed = element.amount * multiplier
                existing_needed = needed.setdefault(element.name, 0)
                total_needed = element_needed + existing_needed

                existing_have = have.setdefault(element.name, 0)
                can_use = min(existing_have, total_needed)
                existing_have -= can_use
                total_needed -= can_use

                needed[element.name] = total_needed
                have[element.name] = existing_have

                if needed[element.name] == 0:
                    del needed[element.name]

        return ore


if __name__ == '__main__':
    code = Y2019D14("2019/14.txt")
    code.part1()
    code.part2()
