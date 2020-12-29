from __future__ import annotations
import re
from queue import Queue
from typing import Set, FrozenSet

from aoc.util.inputs import Input


class BridgeSearch(object):
    def __init__(self, available_bridges: Set[FrozenSet[int]]):
        self._available_bridges = available_bridges.copy()
        self._bridges = []
        self.latest_value = 0

    @property
    def strength(self) -> int:
        return sum(sum(bridge) if len(bridge) == 2 else 2 * sum(bridge) for bridge in self._bridges)

    @property
    def length(self):
        return 2 * len(self._bridges)

    def can_add(self, bridge: FrozenSet[int]) -> bool:
        if len(self._bridges) == 0:
            return 0 in bridge

        previous_bridge = self._bridges[-1]
        if len(bridge.intersection(previous_bridge)) == 0:
            return False

        if bridge not in self._available_bridges:
            return False

        return True

    def add(self, bridge: FrozenSet[int]) -> BridgeSearch:
        if not self.can_add(bridge):
            raise ValueError(f"Cannot add bridge: {bridge}")

        result = BridgeSearch(self._available_bridges)
        result._bridges = self._bridges.copy()
        result._bridges.append(bridge)
        result._available_bridges.remove(bridge)

        if len(bridge) == 1:
            result.latest_value = self.latest_value
        else:
            result.latest_value = list(x for x in bridge if x != self.latest_value)[0]

        return result


class Y2017D24(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        all_bridges = set()
        bridge_map = {}

        for line in lines:
            matched = re.match(r'(\d+)/(\d+)', line)
            start = int(matched.group(1))
            end = int(matched.group(2))
            bridge = frozenset({start, end})

            bridge_map.setdefault(start, set()).add(bridge)
            bridge_map.setdefault(end, set()).add(bridge)
            all_bridges.add(bridge)

        self.strongest_overall_bridge = 0
        longest_bridge = 0
        self.longest_bridge_strength = 0

        queue = Queue()
        queue.put(BridgeSearch(all_bridges))

        while not queue.empty():
            search: BridgeSearch = queue.get()
            self.strongest_overall_bridge = max(self.strongest_overall_bridge, search.strength)

            if search.length > longest_bridge:
                longest_bridge = search.length
                self.longest_bridge_strength = 0

            if search.length == longest_bridge:
                self.longest_bridge_strength = max(self.longest_bridge_strength, search.strength)

            possible_bridges = bridge_map[search.latest_value]

            for bridge in possible_bridges:
                if search.can_add(bridge):
                    queue.put(search.add(bridge))

    def part1(self):
        result = self.strongest_overall_bridge

        print("Part 1:", result)

    def part2(self):
        result = self.longest_bridge_strength

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2017D24("2017/24.txt")
    code.part1()
    code.part2()
