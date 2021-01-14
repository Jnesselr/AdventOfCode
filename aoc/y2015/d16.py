import re
from typing import Dict

from aoc.util.inputs import Input


class Y2015D16(object):
    search = {
        "children": 3,
        "cats": 7,
        "samoyeds": 2,
        "pomeranians": 3,
        "akitas": 0,
        "vizslas": 0,
        "goldfish": 5,
        "trees": 3,
        "cars": 2,
        "perfumes": 1,
    }

    def __init__(self, file_name):
        lines = Input(file_name).lines()

        self.aunts: Dict[int, Dict[str, int]] = {}

        for line in lines:
            sue, facts = re.match(r'Sue (\d+): (.*)', line).groups()
            sue_num = int(sue)

            for fact_kv in facts.split(', '):
                fact, amount = fact_kv.split(": ")
                self.aunts.setdefault(sue_num, {})[fact] = int(amount)

    def part1(self):
        result = 0

        for sue, facts in self.aunts.items():
            valid_sue = True
            for fact, amount in facts.items():
                if fact in self.search and self.search[fact] != amount:
                    valid_sue = False
            if valid_sue:
                result = sue
                break

        print("Part 1:", result)

    def part2(self):
        result = 0

        for sue, facts in self.aunts.items():
            valid_sue = True
            for fact, amount in facts.items():
                if fact in ["cats", "trees"]:
                    valid_sue &= amount > self.search[fact]
                elif fact in ["pomeranians", "goldfish"]:
                    valid_sue &= amount < self.search[fact]
                elif fact in self.search and self.search[fact] != amount:
                    valid_sue = False
            if valid_sue:
                result = sue
                break

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2015D16("2015/16.txt")
    code.part1()
    code.part2()
