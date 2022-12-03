from aoc.util.inputs import Input


class Y2022D2(object):
    _score_dictionary = {
        'A': {  # Their Rock
            'X': 1 + 3,  # My Rock
            'Y': 2 + 6,  # My Paper
            'Z': 3 + 0,  # My Scissors
        },
        'B': {  # Their Paper
            'X': 1 + 0,  # My Rock
            'Y': 2 + 3,  # My Paper
            'Z': 3 + 6,  # My Scissors
        },
        'C': {  # Their Scissors
            'X': 1 + 6,  # My Rock
            'Y': 2 + 0,  # My Paper
            'Z': 3 + 3,  # My Scissors
        },
    }

    _end_dictionary = {
        'A': {  # Their Rock
            'X': 3 + 0,  # Lose, my scissors
            'Y': 1 + 3,  # Draw, my rock
            'Z': 2 + 6,  # Win, my paper
        },
        'B': {  # Their Paper
            'X': 1 + 0,  # Lose, my rock
            'Y': 2 + 3,  # Draw, my paper
            'Z': 3 + 6,  # Win, my scissors
        },
        'C': {  # Their Scissors
            'X': 2 + 0,  # Lose, my paper
            'Y': 3 + 3,  # Draw, my scissors
            'Z': 1 + 6,  # Win, my rock
        },
    }

    def __init__(self, file_name):
        self._games = Input(file_name).lines()

    def part1(self):
        result = 0

        for game in self._games:
            their_play, my_play = game.split(' ')
            result += self._score_dictionary[their_play][my_play]

        print("Part 1:", result)

    def part2(self):
        result = 0

        for game in self._games:
            their_play, my_play = game.split(' ')
            result += self._end_dictionary[their_play][my_play]

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2022D2("2022/2.txt")
    code.part1()
    code.part2()
