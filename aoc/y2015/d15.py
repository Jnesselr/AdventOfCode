import itertools
import re
from dataclasses import dataclass

from aoc.util.inputs import Input


@dataclass(frozen=True)
class Ingredient(object):
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int


class Y2015D15(object):
    regex = re.compile(r'(\w+): capacity (\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (\d+)')

    def __init__(self, file_name):
        lines = Input(file_name).lines()

        self.ingredients = set()

        for line in lines:
            matched = self.regex.match(line)
            self.ingredients.add(Ingredient(
                name=matched.group(1),
                capacity=int(matched.group(2)),
                durability=int(matched.group(3)),
                flavor=int(matched.group(4)),
                texture=int(matched.group(5)),
                calories=int(matched.group(6))
            ))

        self.best_recipe = 0
        self.bast_with_calorie_limitation = 0

        for multipliers in itertools.product(range(101), repeat=len(self.ingredients)):
            if sum(multipliers) != 100:
                continue

            capacity = max(0, sum(i.capacity * m for i, m in zip(self.ingredients, multipliers)))
            durability = max(0, sum(i.durability * m for i, m in zip(self.ingredients, multipliers)))
            flavor = max(0, sum(i.flavor * m for i, m in zip(self.ingredients, multipliers)))
            texture = max(0, sum(i.texture * m for i, m in zip(self.ingredients, multipliers)))
            calories = max(0, sum(i.calories * m for i, m in zip(self.ingredients, multipliers)))

            score = capacity * durability * flavor * texture
            self.best_recipe = max(self.best_recipe, score)

            if calories == 500:
                self.bast_with_calorie_limitation = max(self.bast_with_calorie_limitation, score)

    def part1(self):
        result = self.best_recipe

        print("Part 1:", result)

    def part2(self):
        result = self.bast_with_calorie_limitation

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2015D15("2015/15.txt")
    code.part1()
    code.part2()
