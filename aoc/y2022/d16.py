import itertools
import re
from collections import Counter
from dataclasses import dataclass, field
from queue import Queue
from typing import Dict, Set

from aoc.util.graph import Graph
from aoc.util.inputs import Input


# State always ends with current_valve having been opened, though not necessarily on that turn
@dataclass(frozen=True)
class State:
    current_valve: str
    to_visit: tuple
    opened: tuple
    minutes_remaining: int
    pressure_released: int


class Y2022D16(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()

        self.graph: Graph[str] = Graph[str](directional=True)
        self.flow_rate: Dict[str, int] = {}

        line_re = re.compile(r'Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)')
        for line in lines:
            match = line_re.match(line)
            name = match.group(1)
            flow = int(match.group(2))
            outgoing = match.group(3).split(', ')

            self.flow_rate[name] = flow
            for out in outgoing:
                self.graph.add(name, out)

        what_to_keep = [name for name, flow in self.flow_rate.items() if flow > 0]
        # AA doesn't have a flow rate in the example or my input, so we keep it in the graph to get the new nodes from
        # aa, then we remove it.
        self.graph.compress('AA', *what_to_keep)  # We need to figure out what compressed connections come from AA

        self.nodes_from_aa = {}  # valve -> weight
        for edge in self.graph.edges_from('AA'):
            self.nodes_from_aa[edge.end] = edge.weight

        self.graph.compress(*what_to_keep)  # We no longer need AA, it's flow rate is 0 in both sample and main problem
        self.graph.interconnect()  # We want to be able to jump from any node to any other node in the shortest distance

    def _get_all_states(self, starting_time: int) -> set[State]:
        starting_states = []
        for valve_name in self.nodes_from_aa.keys():
            to_visit = self.graph.all_nodes

            pressure_released = 0

            to_visit.remove(valve_name)
            # It took the weight minutes to get to this valve and 1 to open
            minutes_remaining = starting_time - self.nodes_from_aa[valve_name] - 1
            pressure_released += minutes_remaining * self.flow_rate[valve_name]

            starting_states.append(State(
                current_valve=valve_name,
                minutes_remaining=minutes_remaining,
                to_visit=tuple(to_visit),
                opened=(valve_name,),
                pressure_released=pressure_released
            ))

        q = Queue()
        seen = set()
        for s in starting_states:
            q.put(s)
            seen.add(s)

        most_pressure = 0

        while not q.empty():
            state: State = q.get()
            most_pressure = max(most_pressure, state.pressure_released)

            if len(state.to_visit) == 0:
                continue
            for edge in self.graph.edges_from(state.current_valve):
                if edge.end not in state.to_visit:
                    continue

                # It took edge.weight minutes to get to this valve and 1 to open
                minutes_remaining = state.minutes_remaining - edge.weight - 1

                if minutes_remaining < 0:
                    continue  # Don't bother, this one's a dud

                to_visit = set(state.to_visit)
                to_visit.remove(edge.end)  # No need to visit this node
                visited = list(state.opened)  # Maintain order
                visited.append(edge.end)

                new_state = State(
                    current_valve=edge.end,
                    minutes_remaining=minutes_remaining,
                    to_visit=tuple(to_visit),
                    opened=tuple(visited),
                    pressure_released=state.pressure_released + minutes_remaining * self.flow_rate[edge.end]
                )

                if new_state not in seen:
                    seen.add(new_state)
                    q.put(new_state)

        return seen

    def part1(self):
        states = self._get_all_states(30)
        result = max(s.pressure_released for s in states)

        print("Part 1:", result)

    def part2(self):
        states: set[State] = self._get_all_states(26)

        result = 0

        opened_to_max_value = Counter()
        for state in states:
            opened_state = frozenset(state.opened)
            opened_to_max_value[opened_state] = max(state.pressure_released, opened_to_max_value[opened_state])

        s_human: frozenset[str]
        s_elephant: frozenset[str]
        for s_human, s_elephant in itertools.product(opened_to_max_value.keys(), repeat=2):
            opened_all = set(s_human).union(s_elephant)
            if len(opened_all) < len(s_human) + len(s_elephant):
                continue

            total_pressure_released = opened_to_max_value[s_human] + opened_to_max_value[s_elephant]
            result = max(result, total_pressure_released)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2022D16("2022/16.txt")
    code.part1()
    code.part2()
