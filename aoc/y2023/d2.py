import re
from dataclasses import dataclass
from typing import List

from aoc.util.inputs import Input


@dataclass
class Draw:
    red: int
    green: int
    blue: int


@dataclass
class Game:
    game_number: int
    draws: List[Draw]


class Y2023D2(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.games = []

        line_re = re.compile(r"Game (\d+): (.*)")
        for line in lines:
            match = line_re.match(line)
            game_number = int(match.group(1))
            draws = match.group(2).split('; ')

            game = Game(game_number, [])
            for draw in draws:
                rgb_values = draw.split(', ')
                red = green = blue = 0
                for rgb_value in rgb_values:
                    rgb_number = int(rgb_value.split(' ')[0])
                    if rgb_value.endswith('red'):
                        red = rgb_number
                    elif rgb_value.endswith('green'):
                        green = rgb_number
                    elif rgb_value.endswith('blue'):
                        blue = rgb_number

                game.draws.append(Draw(
                    red=red,
                    green=green,
                    blue=blue,
                ))

            self.games.append(game)

    def part1(self):
        result = 0

        max_red_cubes = 12
        max_green_cubes = 13
        max_blue_cubes = 14

        for game in self.games:
            invalid_game = any(
                x.red > max_red_cubes or x.green > max_green_cubes or x.blue > max_blue_cubes for x in game.draws
            )
            if not invalid_game:
                result += game.game_number

        print("Part 1:", result)

    def part2(self):
        result = 0

        for game in self.games:
            min_required_red = max(x.red for x in game.draws)
            min_required_green = max(x.green for x in game.draws)
            min_required_blue = max(x.blue for x in game.draws)
            result += min_required_red * min_required_green * min_required_blue

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2023D2("2023/2.txt")
    code.part1()
    code.part2()
