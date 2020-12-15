from typing import Dict

from aoc.util.inputs import Input


class Y2020D15(object):
    def __init__(self, file_name):
        line = Input(file_name).line()
        self.starting = [int(x) for x in line.split(',')]

    def part1(self):
        result = self.play_game(2020)

        print("Part 1:", result)

    def part2(self):
        result = self.play_game(30000000)

        print("Part 2:", result)

    def play_game(self, last_turn):
        game_last: Dict[int, int] = {}
        game_before: Dict[int, int] = {}
        turn = 1
        last_spoken = None
        for i in self.starting:
            game_last[i] = turn
            turn += 1
            last_spoken = i
        while turn <= last_turn:
            if last_spoken not in game_before:  # First time spoken
                if 0 in game_last:
                    game_before[0] = game_last[0]
                game_last[0] = turn
                last_spoken = 0
            else:
                last_spoken = game_last[last_spoken] - game_before[last_spoken]
                if last_spoken in game_last:
                    game_before[last_spoken] = game_last[last_spoken]
                game_last[last_spoken] = turn

            turn += 1
        return last_spoken


if __name__ == '__main__':
    code = Y2020D15("2020/15.txt")
    code.part1()
    code.part2()
