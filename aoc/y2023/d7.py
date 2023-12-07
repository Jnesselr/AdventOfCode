import enum
from collections import Counter
from functools import cached_property

from aoc.util.inputs import Input


class Rank(enum.Enum):
    FIVE_OF_A_KIND = 6
    FOUR_OF_A_KIND = 5
    FULL_HOUSE = 4
    THREE_OF_A_KIND = 3
    TWO_PAIR = 2
    ONE_PAIR = 1
    HIGH_CARD = 0


class Hand:
    def __init__(self, values: str, bid: int, jokers_are_wild=False):
        self._cards: str = values
        self._bid: int = bid
        self._jokers_are_wild = jokers_are_wild

    @property
    def cards(self) -> str:
        return self._cards

    @property
    def bid(self) -> int:
        return self._bid

    def __str__(self) -> str:
        return f"{self._cards} ({self.rank})"

    @property
    def make_wild(self) -> 'Hand':
        return Hand(self._cards, self._bid, jokers_are_wild=True)

    @cached_property
    def rank(self) -> Rank:
        counter = Counter()

        for c in self._cards:
            counter[c] += 1

        if self._jokers_are_wild:
            joker_count = counter['J']
            if len(counter) > 1:  # Avoid the all joker special case
                del counter['J']
                max_entry = counter.most_common(1)[0]
                counter[max_entry[0]] += joker_count

        if [True for v in counter.values() if v == 5]:
            return Rank.FIVE_OF_A_KIND
        elif [True for v in counter.values() if v == 4]:
            return Rank.FOUR_OF_A_KIND
        elif [True for v in counter.values() if v == 3] and [True for v in counter.values() if v == 2]:
            return Rank.FULL_HOUSE
        elif [True for v in counter.values() if v == 3]:
            return Rank.THREE_OF_A_KIND
        elif len([True for v in counter.values() if v == 2]) == 2:
            return Rank.TWO_PAIR
        elif [True for v in counter.values() if v == 2]:
            return Rank.ONE_PAIR
        else:
            return Rank.HIGH_CARD

    def __lt__(self, other: 'Hand') -> bool:
        if self.rank.value < other.rank.value:
            return True

        if other.rank.value < self.rank.value:
            return False

        if self._jokers_are_wild:
            __card_order = 'AKQT98765432J'
        else:
            __card_order = 'AKQJT98765432'

        # Same rank, order by cards
        for lvalue, rvalue in zip(self._cards, other._cards):
            l_index = __card_order.index(lvalue)
            r_index = __card_order.index(rvalue)
            if l_index == r_index:
                continue  # Same rank, continue
            elif l_index < r_index:
                return False  # We're higher ranked, so other is less than us
            elif l_index > r_index:
                return True  # We're lower ranked, so other is greater than us

        return False  # We shouldn't get here based on the criteria given

    def __eq__(self, other: 'Hand') -> bool:
        return self._cards == other._cards  # Same cards, same rank score


class Y2023D7(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.hands = []

        for line in lines:
            hand_values, bid = line.split(' ')
            bid = int(bid)
            hand = Hand(hand_values, bid)
            self.hands.append(hand)

    def part1(self):
        result = self.determine_score(self.hands)

        print("Part 1:", result)

    def part2(self):
        result = self.determine_score([h.make_wild for h in self.hands])

        print("Part 2:", result)

    @staticmethod
    def determine_score(hands):
        hands = sorted(hands)
        result = 0
        for rank, hand in enumerate(hands):
            result += (rank + 1) * hand.bid
        return result


if __name__ == '__main__':
    code = Y2023D7("2023/7.txt")
    code.part1()
    code.part2()
