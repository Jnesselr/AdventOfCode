import itertools
import re
from typing import Dict

from aoc.util.graph import Graph
from aoc.util.inputs import Input


class Y2015D13(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()

        self.graph: Graph[str] = Graph[str]()
        self.all_people = set()

        units: Dict[str, Dict[str, int]] = {}
        for line in lines:
            matched = re.match(r'(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+).', line)
            _from = matched.group(1)
            _to = matched.group(4)
            happiness = int(matched.group(3))

            if matched.group(2) == "lose":
                happiness = -happiness

            units.setdefault(_from, {})[_to] = happiness
            self.all_people.add(_from)
            self.all_people.add(_to)

        for _from, _to in itertools.permutations(self.all_people, r=2):
            happiness = units.setdefault(_from, {}).setdefault(_to, 0) + \
                        units.setdefault(_to, {}).setdefault(_from, 0)
            self.graph.add(_from, _to, happiness)

    def part1(self):
        result = self.graph.highest_tsp(loop=True)

        print("Part 1:", result)

    def part2(self):
        for person in self.all_people:
            self.graph.add("me", person, 0)

        result = self.graph.highest_tsp(loop=True)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2015D13("2015/13.txt")
    code.part1()
    code.part2()
