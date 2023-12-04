import re
from collections import Counter
from dataclasses import dataclass

from aoc.util.inputs import Input


@dataclass
class Card:
    number: int
    winning: frozenset[int]
    have: frozenset[int]

    @property
    def worth(self) -> int:
        points = 0

        for winner in self.winning:
            if winner in self.have:
                if points == 0:
                    points = 1
                else:
                    points *= 2

        return points

    @property
    def winning_numbers(self) -> int:
        winning_numbers = 0

        for winner in self.winning:
            if winner in self.have:
                winning_numbers += 1

        return winning_numbers


class Y2023D4(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()

        line_re = re.compile(r'Card\s+(\d+): (.*) \| (.*)')
        self.cards: list[Card] = []
        for line in lines:
            match = line_re.match(line)
            card = Card(number=int(match.group(1)),
                        winning=self._to_set(match.group(2)),
                        have=self._to_set(match.group(3))
                        )
            self.cards.append(card)

    @staticmethod
    def _to_set(numbers: str) -> frozenset:
        reduced = numbers.strip(' ').replace('  ', ' ')
        while len(reduced) != len(numbers):
            numbers = reduced
            reduced = numbers.replace('  ', ' ')

        return frozenset([int(x) for x in numbers.split(' ')])

    def part1(self):
        result = sum(card.worth for card in self.cards)

        print("Part 1:", result)

    def part2(self):
        scratchcards = Counter()
        for card in self.cards:
            scratchcards[card.number] += 1  # Original card
            copies_of_this_card = scratchcards[card.number]
            if copies_of_this_card == 0:
                break
            for i in range(card.winning_numbers):
                scratchcards[card.number + i + 1] += copies_of_this_card

        result = sum(v for v in scratchcards.values())

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2023D4("2023/4.txt")
    code.part1()
    code.part2()
