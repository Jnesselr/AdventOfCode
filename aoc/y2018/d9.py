from __future__ import annotations
import re

from aoc.util.inputs import Input


class Marble(object):
    def __init__(self, value: int):
        self.value = value
        self.prev: Marble = self
        self.next: Marble = self

    def append(self, value: int) -> Marble:
        next_marble = self.next
        new_marble = Marble(value)

        new_marble.next = next_marble
        next_marble.prev = new_marble

        new_marble.prev = self
        self.next = new_marble

        return new_marble

    def remove(self) -> None:
        prev_marble = self.prev
        next_marble = self.next

        prev_marble.next = next_marble
        next_marble.prev = prev_marble


class Game(object):
    def __init__(self, players, last_marble_value):
        self.players = players
        self.last_marble_value = last_marble_value
        self.current_marble: Marble = Marble(0)

        self._scores = dict((x, 0) for x in range(0, players))
        self._current_player = 0

    def play(self):
        for marble_value in range(1, self.last_marble_value+1):
            if marble_value % 23 == 0:
                # 7 counter clockwise is the removed one, 6 is the current.
                self.current_marble = self.current_marble.prev.prev.prev.prev.prev.prev
                removed_marble = self.current_marble.prev
                self._scores[self._current_player] += marble_value + removed_marble.value

                removed_marble.remove()
            else:
                self.current_marble: Marble = self.current_marble.next.append(marble_value)

            self._current_player = (self._current_player + 1) % self.players

    def highest_score(self) -> int:
        _, score = max(self._scores.items(), key=lambda x: x[1])
        return score


class Y2018D9(object):
    def __init__(self, file_name):
        line = Input(file_name).line()
        matched = re.match(r"(\d+) players; last marble is worth (\d+) points", line)
        self.players = int(matched.group(1))
        self.last_marble = int(matched.group(2))

    def part1(self):
        game = Game(self.players, self.last_marble)
        game.play()
        result = game.highest_score()

        print("Part 1:", result)

    def part2(self):
        game = Game(self.players, self.last_marble * 100)
        game.play()
        result = game.highest_score()

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2018D9("2018/9.txt")
    code.part1()
    code.part2()
