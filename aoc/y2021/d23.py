from dataclasses import dataclass
from typing import FrozenSet, Iterable, Dict, Set, Tuple, List

from aoc.util.coordinate import Coordinate, CoordinateSystem
from aoc.util.graph import Edge, Graph
from aoc.util.grid import Grid
from aoc.util.inputs import Input
from aoc.util.queue import PriorityQueue


# State assumes the hallway and where the burrows are the same everywhere
@dataclass(frozen=True)
class State(object):
    COST = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
    HALLWAY_MOVES = [0, 1, 3, 5, 7, 9, 10]
    WANT_TO_GO = {'A': 2, 'B': 4, 'C': 6, 'D': 8}
    BURROWS_INDEX = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    INDEX_BURROWS = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
    INDEX_BURROW_TO_INDEX_HALLWAY = {0: 2, 1: 4, 2: 6, 3: 8}

    hallway: str
    burrows: Tuple[str]
    cost: int

    def expand(self) -> 'State':
        return State(
            hallway=self.hallway,
            burrows=(
                self.burrows[0][0] + 'DD' + self.burrows[0][1],
                self.burrows[1][0] + 'CB' + self.burrows[1][1],
                self.burrows[2][0] + 'BA' + self.burrows[2][1],
                self.burrows[3][0] + 'AC' + self.burrows[3][1],
            ),
            cost=self.cost
        )
        pass

    @property
    def completed(self) -> bool:
        return all(r == 'A' for r in self.burrows[0]) \
               and all(r == 'B' for r in self.burrows[1]) \
               and all(r == 'C' for r in self.burrows[2]) \
               and all(r == 'D' for r in self.burrows[3])

    def available(self) -> Iterable['State']:
        # Moving from burrows to hallway
        for burrow_index, burrow in enumerate(self.burrows):
            amphipod_type = self.INDEX_BURROWS[burrow_index]
            all_settled = all(c in ['.', amphipod_type] for c in burrow)
            if all_settled:
                continue

            if '.' in burrow:
                last_empty = burrow.rindex('.')
            else:
                last_empty = -1
            if last_empty + 1 == len(burrow):
                continue

            moving_amphipod = burrow[last_empty + 1]

            starting_column = self.INDEX_BURROW_TO_INDEX_HALLWAY[burrow_index]
            for to_go in self.HALLWAY_MOVES:
                if not self._can_move_in_hallway(starting_column, to_go):
                    continue

                extra_cost = self.COST[moving_amphipod] * (abs(to_go - starting_column) + (last_empty + 2))

                yield self._new_state(extra_cost, to_go, burrow_index)

        # Moving from hallway to burrows
        for hall_index, amphipod in enumerate(self.hallway):
            if amphipod == '.':
                continue

            to_go = self.WANT_TO_GO[amphipod]

            can_move = self._can_move_in_hallway(hall_index, to_go)
            target_index = self.BURROWS_INDEX[amphipod]
            target_burrow: str = self.burrows[target_index]
            can_move &= all(c == '.' or c == amphipod for c in target_burrow)

            if not can_move:
                continue

            replacement_index = target_burrow.rindex('.')
            extra_cost = self.COST[amphipod] * (abs(to_go - hall_index) + (replacement_index + 1))

            yield self._new_state(extra_cost, hall_index, target_index)

    def _can_move_in_hallway(self, start: int, end: int) -> bool:
        left = min(start, end)
        right = max(start, end)
        return all(self.hallway[i] == '.' for i in range(left, right + 1) if i != start)

    def _new_state(self,
                   extra_cost: int,
                   hallway_index: int,
                   burrow_index: int) -> 'State':
        burrow = self.burrows[burrow_index]

        if self.hallway[hallway_index] == '.':
            b_index, amphipod = [(i, c) for i, c in enumerate(burrow) if c != '.'][0]
            new_hallway = self.hallway[:hallway_index] + amphipod + self.hallway[hallway_index + 1:]
            new_burrow = burrow[:b_index] + '.' + burrow[b_index + 1:]
        else:
            amphipod = self.hallway[hallway_index]
            b_index = [i for i, c in enumerate(burrow) if c == '.'][-1]
            new_hallway = self.hallway[:hallway_index] + '.' + self.hallway[hallway_index + 1:]
            new_burrow = burrow[:b_index] + amphipod + burrow[b_index + 1:]

        new_burrows_list = list(self.burrows[:burrow_index])
        new_burrows_list.append(new_burrow)
        new_burrows_list.extend(self.burrows[burrow_index + 1:])

        return State(
            hallway=new_hallway,
            burrows=tuple(new_burrows_list),
            cost=self.cost + extra_cost
        )


class Y2021D23(object):
    def __init__(self, file_name):
        grid: Grid[str] = Input(file_name).grid()

        existing_amphipods = grid.find(lambda value: value in 'ABCD')

        _burrow_top = min(a.y for a in existing_amphipods)
        _burrow_bottom = max(a.y for a in existing_amphipods)

        burrows = [''] * 4
        for y in range(_burrow_top, _burrow_bottom + 1):
            for index, x in enumerate([3, 5, 7, 9]):
                to_push = grid[x, y]
                burrows[index] += to_push

        self._starting_state = State(
            hallway='.' * len(grid.find('.')),
            burrows=tuple(burrows),
            cost=0
        )

    def part1(self):
        result = self._find_min_cost(self._starting_state)

        print("Part 1:", result)

    def part2(self):
        result = self._find_min_cost(self._starting_state.expand())

        print("Part 2:", result)

    @staticmethod
    def _find_min_cost(starting_state):
        result = 0

        seen: Set[State] = {starting_state}
        queue: PriorityQueue[State] = PriorityQueue[State]()
        queue.push(starting_state, starting_state.cost)

        while not queue.empty:
            state = queue.pop()
            # print(state)

            if state.completed:
                result = state.cost
                min_result = state
                # print("Updated min score!:", result, state.cost)
                break

            for possible in state.available():
                if possible in seen:
                    # print(f"Already in seen {possible}")
                    continue

                seen.add(possible)
                queue.push(possible, possible.cost)

        return result


if __name__ == '__main__':
    code = Y2021D23("2021/23.txt")
    code.part1()
    code.part2()
