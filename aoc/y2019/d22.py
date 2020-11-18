import re
from dataclasses import dataclass

from aoc.util.inputs import Input

# The math is explained here: https://www.reddit.com/r/adventofcode/comments/ee0rqi/2019_day_22_solutions/fbnkaju/


@dataclass(frozen=True)
class Deck(object):
    cards: int
    offset: int = 0
    increment: int = 1

    def __getitem__(self, item):
        return (self.offset + (self.increment * item)) % self.cards

    def new_stack(self):
        new_increment = -self.increment
        new_offset = self.offset + new_increment
        return Deck(cards=self.cards, offset=new_offset, increment=new_increment)

    def cut(self, n):
        new_offset = self.offset + self.increment * n

        return Deck(cards=self.cards, offset=new_offset, increment=self.increment)

    def _inv(self, n):
        return pow(n, self.cards - 2, self.cards)

    def deal_increment(self, increment):
        new_increment = self.increment * self._inv(increment)

        return Deck(cards=self.cards, offset=self.offset, increment=new_increment)

    def shuffle(self, num_times):
        new_increment = pow(self.increment, num_times, self.cards)
        new_offset = self.offset * (1 - pow(self.increment, num_times, self.cards)) * self._inv(1 - self.increment)

        return Deck(cards=self.cards, offset=new_offset, increment=new_increment)


class Y2019D22(object):
    def __init__(self, file_name):
        self.operations = Input(file_name).lines()

    def part1(self):
        deck = Deck(10007)
        deck = self._shuffle(deck)
        result = -1
        for i in range(deck.cards):
            if deck[i] == 2019:
                result = i
                break

        print("Part 1:", result)

    def part2(self):
        deck = Deck(119315717514047)
        deck = self._shuffle(deck)
        deck = deck.shuffle(101741582076661)
        result = deck[2020]

        print("Part 2:", result)

    def _shuffle(self, deck: Deck) -> Deck:
        for operation in self.operations:
            cut_match = re.match(r"cut (-?\d+)", operation)
            increment = re.match(r"deal with increment (-?\d+)", operation)
            if cut_match is not None:
                deck = deck.cut(int(cut_match.group(1)))
            elif increment is not None:
                deck = deck.deal_increment(int(increment.group(1)))
            else:
                deck = deck.new_stack()
        return deck


if __name__ == '__main__':
    code = Y2019D22("2019/22.txt")
    code.part1()
    code.part2()
