import re
from dataclasses import dataclass
from typing import Set, Dict

from aoc.util.inputs import Input
from aoc.util.possibility_reducer import reduce_possibilities


@dataclass
class Food(object):
    ingredients: Set[str]
    allergens: Set[str]


class Y2020D21(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.foods = []
        self.all_allergens = set()
        self.all_ingredients = set()

        for line in lines:
            matched = re.match(r'([ \w]+) \(contains ([ ,\w]+)\)', line)
            allergens = set(matched.group(2).split(', '))
            ingredients = set(matched.group(1).split(' '))
            self.foods.append(Food(
                ingredients=ingredients,
                allergens=allergens
            ))
            self.all_ingredients = self.all_ingredients.union(ingredients)
            self.all_allergens = self.all_allergens.union(allergens)

        allergen_to_ingredients: Dict[str, Set[str]] = {}

        for allergen in self.all_allergens:
            names = None
            for food in self.foods:
                if allergen in food.allergens:
                    if names is None:
                        names = set(food.ingredients)
                    else:
                        names = names.intersection(set(food.ingredients))
            allergen_to_ingredients[allergen] = names

        self.known_allergens: Dict[str, str] = reduce_possibilities(allergen_to_ingredients)

    def part1(self):
        good_ingredients = self.all_ingredients - set(self.known_allergens.values())
        result = 0
        for food in self.foods:
            ingredients = good_ingredients.intersection(food.ingredients)
            result += len(ingredients)

        print("Part 1:", result)

    def part2(self):
        result = []
        for allergen in sorted(self.known_allergens.keys()):
            result.append(self.known_allergens[allergen])

        result = ",".join(result)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2020D21("2020/21.txt")
    code.part1()
    code.part2()
