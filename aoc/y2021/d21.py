import re
from dataclasses import field, dataclass
from queue import Queue
from typing import Dict

from aoc.util.inputs import Input


class DeterministicDice(object):
    def __init__(self):
        self._value = 1
        self._times_rolled = 0

    @property
    def times_rolled(self):
        return self._times_rolled

    def __iter__(self):
        return self

    def __next__(self):
        result = self._value
        self._times_rolled += 1
        self._value += 1

        if self._value == 101:
            self._value = 1

        return result


@dataclass(frozen=True)
class UniverseGameState(object):
    player: int
    player_1_position: int
    player_2_position: int
    universes: int = field(default=1)
    player_1_score: int = field(default=0)
    player_2_score: int = field(default=0)


class Y2021D21(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self._starting_positions = {}

        player_position_regex = re.compile(r'Player (\d+) starting position: (\d+)')
        for line in lines:
            match = player_position_regex.match(line)
            self._starting_positions[int(match.group(1))] = int(match.group(2))

    def part1(self):
        dice = DeterministicDice()
        player_scores: Dict[int, int] = dict((player, 0) for player in self._starting_positions.keys())
        player_positions: Dict[int, int] = dict(
            (player, position) for player, position in self._starting_positions.items())
        player = 1

        while all(score < 1000 for score in player_scores.values()):
            roll = next(dice) + next(dice) + next(dice)
            position = player_positions[player]
            position += roll

            if position > 10:
                position = position % 10

            if position == 0:
                position = 10

            player_scores[player] += position
            player_positions[player] = position

            player = 2 if player == 1 else 1

        result = min(player_scores.values()) * dice.times_rolled

        print("Part 1:", result)

    def part2(self):
        player_1_total_wins = 0
        player_2_total_wins = 0

        starting_game = UniverseGameState(
            player=1,
            player_1_position=self._starting_positions[1],
            player_2_position=self._starting_positions[2],
        )
        queue = Queue()
        queue.put(starting_game)

        # Dice roll to how many universes are made for that dice roll
        universe_split = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}

        while not queue.empty():
            print(queue.qsize(), player_1_total_wins, player_2_total_wins)
            game: UniverseGameState = queue.get()

            for roll, universe_multiplier in universe_split.items():
                position = game.player_1_position if game.player == 1 else game.player_2_position
                position += roll

                if position > 10:
                    position = position % 10

                if position == 0:
                    position = 10

                score = game.player_1_score if game.player == 1 else game.player_2_score
                score += position
                universes = game.universes * universe_multiplier

                new_universe = UniverseGameState(
                    player=(2 if game.player == 1 else 1),
                    player_1_position=(position if game.player == 1 else game.player_1_position),
                    player_1_score=(score if game.player == 1 else game.player_1_score),
                    player_2_position=(position if game.player == 2 else game.player_2_position),
                    player_2_score=(score if game.player == 2 else game.player_2_score),
                    universes=universes
                )

                if new_universe.player_1_score >= 21:
                    player_1_total_wins += new_universe.universes
                    continue
                elif new_universe.player_2_score >= 21:
                    player_2_total_wins += new_universe.universes
                    continue
                else:
                    queue.put(new_universe)

        result = max(player_1_total_wins, player_2_total_wins)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2021D21("2021/21.txt")
    code.part1()
    code.part2()
