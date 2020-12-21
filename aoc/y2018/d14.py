from aoc.util.inputs import Input


class Y2018D14(object):
    def __init__(self, file_name):
        self.input = Input(file_name).line()
        self.initial_recipe = [3, 7]

    def part1(self):
        first_elf = 0
        second_elf = 1
        recipe = self.initial_recipe.copy()

        input_value = int(self.input)

        while len(recipe) < (input_value + 10):
            new_value = recipe[first_elf] + recipe[second_elf]
            if new_value > 9:
                recipe.append(1)
            recipe.append(new_value % 10)

            recipe_length = len(recipe)
            first_elf = (recipe[first_elf] + 1 + first_elf) % recipe_length
            second_elf = (recipe[second_elf] + 1 + second_elf) % recipe_length

        string = "".join(str(x) for x in recipe[input_value:input_value+10])
        result = string

        print("Part 1:", result)

    def part2(self):
        result = 0
        to_match = [int(x) for x in self.input]
        match_length = len(to_match)

        first_elf = 0
        second_elf = 1
        recipe = self.initial_recipe.copy()

        while True:
            new_value = recipe[first_elf] + recipe[second_elf]
            if new_value > 9:
                recipe.append(1)
            recipe.append(new_value % 10)

            recipe_length = len(recipe)
            first_elf = (recipe[first_elf] + 1 + first_elf) % recipe_length
            second_elf = (recipe[second_elf] + 1 + second_elf) % recipe_length

            if recipe[-match_length:] == to_match:
                result = len(recipe) - match_length
                break
            elif recipe[-match_length-1:-1] == to_match:
                result = len(recipe) - match_length - 1
                break

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2018D14("2018/14.txt")
    code.part1()
    code.part2()
