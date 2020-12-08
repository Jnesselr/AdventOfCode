import re
from dataclasses import dataclass
from typing import Dict

from aoc.util.inputs import Input


@dataclass
class Bag(object):
    name: str
    contains: Dict[str, int]


class Y2020D7(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()

        self.bags = []
        for line in lines:
            name, extra = line.split(" bags contain ")

            contains = {}
            if extra != "no other bags.":
                for bag in extra[:-1].split(', '):
                    matched = re.match(r"(\d+) ([\w ]+) bags?", bag)
                    contains[matched.group(2)] = int(matched.group(1))

            self.bags.append(Bag(name, contains))

    def part1(self):
        bags_that_can_hold_shiny_gold = set()

        something_changed = True
        while something_changed:
            something_changed = False
            holding_bag: Bag
            for holding_bag in self.bags:
                if holding_bag.name in bags_that_can_hold_shiny_gold:
                    continue
                for search_bag in list(bags_that_can_hold_shiny_gold):
                    if search_bag in holding_bag.contains:
                        bags_that_can_hold_shiny_gold.add(holding_bag.name)
                        something_changed = True
                if "shiny gold" in holding_bag.contains:
                    bags_that_can_hold_shiny_gold.add(holding_bag.name)
                    something_changed = True

        print("Part 1:", len(bags_that_can_hold_shiny_gold))

    def part2(self):
        bag_dictionary = dict([(bag.name, bag) for bag in self.bags])
        bags_needed_cache = {}

        def _get_bag_needed_count(bag_name):
            if bag_name in bags_needed_cache:
                return bags_needed_cache[bag_name]

            bag: Bag = bag_dictionary[bag_name]
            bags_needed = 0

            for needed_bag, bag_count in bag.contains.items():
                bags_needed += (_get_bag_needed_count(needed_bag) * bag_count) + bag_count

            bags_needed_cache[bag_name] = bags_needed

            return bags_needed

        result = _get_bag_needed_count("shiny gold")

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2020D7("2020/7.txt")
    code.part1()
    code.part2()
