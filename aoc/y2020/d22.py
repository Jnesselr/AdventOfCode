from queue import Queue
from typing import Tuple, List, Set, Optional

from aoc.util.inputs import Input


class RecursiveCombat(object):
    def __call__(self, player_1_deck: List[int], player_2_deck: List[int]) -> Tuple[int, Optional[List[int]]]:
        player_1 = Queue()
        for card in player_1_deck:
            player_1.put(card)

        player_2 = Queue()
        for card in player_2_deck:
            player_2.put(card)

        seen_rounds: Set[Tuple[str, str]] = set()
        while not player_1.empty() and not player_2.empty():
            seen_tuple = (",".join(str(x) for x in player_1.queue), ",".join(str(x) for x in player_2.queue))

            if seen_tuple in seen_rounds:
                return 1, None
            seen_rounds.add(seen_tuple)

            p1_card: int = player_1.get()
            p2_card: int = player_2.get()

            if p1_card > player_1.qsize() or p2_card > player_2.qsize():
                if p1_card > p2_card:
                    player_1.put(p1_card)
                    player_1.put(p2_card)
                elif p1_card < p2_card:
                    player_2.put(p2_card)
                    player_2.put(p1_card)
            else:
                p1_sub_deck = list(player_1.queue)[:p1_card]
                p2_sub_deck = list(player_2.queue)[:p2_card]

                winner, _ = self(p1_sub_deck, p2_sub_deck)

                if winner == 1:
                    player_1.put(p1_card)
                    player_1.put(p2_card)
                else:
                    player_2.put(p2_card)
                    player_2.put(p1_card)

        if not player_1.empty():
            return 1, list(player_1.queue)

        if not player_2.empty():
            return 2, list(player_2.queue)


class Y2020D22(object):
    def __init__(self, file_name):
        groups = Input(file_name).grouped()
        self.player_1_starting_deck = [int(x) for x in groups[0][1:]]
        self.player_2_starting_deck = [int(x) for x in groups[1][1:]]

    def part1(self):
        player_1 = Queue()
        for card in self.player_1_starting_deck:
            player_1.put(card)

        player_2 = Queue()
        for card in self.player_2_starting_deck:
            player_2.put(card)

        while not player_1.empty() and not player_2.empty():
            p1_card: int = player_1.get()
            p2_card: int = player_2.get()

            if p1_card > p2_card:
                player_1.put(p1_card)
                player_1.put(p2_card)
            elif p1_card < p2_card:
                player_2.put(p2_card)
                player_2.put(p1_card)

        winning_queue = player_1 if not player_1.empty() else player_2
        winning_deck = list(winning_queue.queue)

        result = self._deck_score(winning_deck)

        print("Part 1:", result)

    def part2(self):
        combat = RecursiveCombat()
        winner, deck = combat(self.player_1_starting_deck, self.player_2_starting_deck)

        result = self._deck_score(deck)

        print("Part 2:", result)

    @staticmethod
    def _deck_score(winning_deck):
        result = 0
        winning_deck.reverse()
        for index, card in enumerate(winning_deck):
            result += (index + 1) * card
        return result


if __name__ == '__main__':
    code = Y2020D22("2020/22.txt")
    code.part1()
    code.part2()
