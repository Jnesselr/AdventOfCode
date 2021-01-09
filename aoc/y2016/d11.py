from __future__ import annotations

import itertools
import re
from dataclasses import dataclass, field
from queue import Queue
from typing import FrozenSet, Set, Union, Optional, List, Dict
from typing import Generator as TypeGenerator

from aoc.util.inputs import Input
from aoc.util.queue import PriorityQueue


@dataclass(frozen=True)
class Microchip(object):
    name: str


@dataclass(frozen=True)
class Generator(object):
    name: str


@dataclass(frozen=True)
class Floors(object):
    elevator: int
    f1: FrozenSet[Union[Microchip, Generator]]
    f2: FrozenSet[Union[Microchip, Generator]]
    f3: FrozenSet[Union[Microchip, Generator]]
    f4: FrozenSet[Union[Microchip, Generator]]
    steps: int = field(compare=False)

    def on_floor(self, floor) -> Set[Union[Microchip, Generator]]:
        return set(getattr(self, f'f{floor}'))

    def microchips(self, floor) -> Set[Microchip]:
        return set(x for x in self.on_floor(floor) if isinstance(x, Microchip))

    def generators(self, floor) -> Set[Generator]:
        return set(x for x in self.on_floor(floor) if isinstance(x, Generator))

    @property
    def score(self):
        return len(self.f3) + 2 * len(self.f2) + 3 * len(self.f1)

    @property
    def is_complete(self) -> bool:
        return self.score == 0

    def print(self):
        for floor in range(4, 0, -1):
            to_print = f"F{floor} "
            if floor == self.elevator:
                to_print += "E "
            else:
                to_print += ". "

            floor_microchips = self.microchips(floor)
            floor_generators = self.generators(floor)

            for microchip in floor_microchips:
                to_print += f"{microchip.name[0].upper()}M "

            for generator in floor_generators:
                to_print += f"{generator.name[0].upper()}G "

            print(to_print)

    def options(self) -> TypeGenerator[Floors]:
        if self.elevator > 1:
            yield from self._options(self.elevator - 1)

        if self.elevator < 4:
            yield from self._options(self.elevator + 1)

    def _options(self, new_floor) -> TypeGenerator[Floors]:
        elevator_microchips = self.microchips(self.elevator)
        elevator_generators = self.generators(self.elevator)
        new_floor_microchips = self.microchips(new_floor)
        new_floor_generator_names = set(x.name for x in self.generators(new_floor))

        # Microchips can move by themselves or in pairs as long as that doesn't fry them.
        for x, y in itertools.combinations(elevator_microchips.union({None}), r=2):
            can_move_x = self._can_move_microchip_to(x, new_floor)
            can_move_y = self._can_move_microchip_to(y, new_floor)
            if can_move_x and can_move_y:
                yield self._move(new_floor, x, y)
            if can_move_x and y is None:
                yield self._move(new_floor, x, None)
            if can_move_y and x is None:
                yield self._move(new_floor, y, None)

        elevator_generator_dict = dict((x.name, x) for x in elevator_generators)
        unprotected_micros = set(x for x in new_floor_microchips if x.name not in new_floor_generator_names)

        # A microchip can move with its generator if that doesn't threaten any chips in new floor.
        if len(unprotected_micros) == 0 and self.elevator < new_floor:
            for microchip in elevator_microchips:
                if microchip.name in elevator_generator_dict:
                    matching_generator = elevator_generator_dict[microchip.name]
                    yield self._move(new_floor, microchip, matching_generator)

        # A generator can move if moving those generators protects all micros
        if len(unprotected_micros) <= 2 and new_floor :
            for x, y in itertools.combinations(elevator_generators.union({None}), r=2):
                can_move_generators = self._keeps_microchips_safe(unprotected_micros, x, y)
                if can_move_generators:
                    yield self._move(new_floor, x, y)

    def _move(self,
              new_floor: int,
              item1: Optional[Union[Microchip, Generator]],
              item2: Optional[Union[Microchip, Generator]]):
        floors = {}
        for floor in range(1, 5):
            floors[floor] = self.on_floor(floor)

        if item1 is not None and item1 in floors[self.elevator]:
            floors[self.elevator].remove(item1)
            floors[new_floor].add(item1)

        if item2 is not None and item2 in floors[self.elevator]:
            floors[self.elevator].remove(item2)
            floors[new_floor].add(item2)

        return Floors(
            elevator=new_floor,
            f1=frozenset(floors[1]),
            f2=frozenset(floors[2]),
            f3=frozenset(floors[3]),
            f4=frozenset(floors[4]),
            steps=self.steps + 1
        )

    def _can_move_microchip_to(self, microchip: Optional[Microchip], floor: int) -> bool:
        if microchip is None:
            return False

        floor_generators = self.generators(floor)

        if len(floor_generators) == 0:
            return True

        if microchip.name in [x.name for x in floor_generators]:
            return True

        return False

    @staticmethod
    def _keeps_microchips_safe(unprotected_micros: Set[Microchip],
                               *generators: Generator) -> bool:
        microchip_names = set(x.name for x in unprotected_micros)

        generator: Generator
        for generator in generators:
            if generator is not None and generator.name in microchip_names:
                microchip_names.remove(generator.name)

        return len(microchip_names) == 0


class Y2016D11(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()

        floors: Dict[int, Set[Union[Microchip, Generator]]] = {}

        for line in lines:
            microchip_search = re.findall(r'(\w+)-compatible microchip', line)
            generator_search = re.findall(r'(\w+) generator', line)
            floor = re.search(r'The (\w+) floor', line).group(1)
            floor = {
                "first": 1,
                "second": 2,
                "third": 3,
                "fourth": 4,
            }[floor]
            floors[floor] = set() \
                .union(Microchip(x) for x in microchip_search) \
                .union(Generator(x) for x in generator_search)

        self.floors = Floors(
            elevator=1,
            f1=frozenset(floors[1]),
            f2=frozenset(floors[2]),
            f3=frozenset(floors[3]),
            f4=frozenset(floors[4]),
            steps=0
        )

    def part1(self):
        start_floors = self.floors
        best_floor = self.get_min_steps_to_top_floor(start_floors)

        result = best_floor.steps
        best_floor.print()
        print()

        print("Part 1:", result)

    # TODO Improve this a lot. Right now, it takes ~7 hours to find a solution.
    def part2(self):
        new_1st_floor = set(self.floors.f1).union({
            Microchip("elerium"), Generator("elerium"),
            Microchip("dilithium"), Generator("dilithium")
        })
        start_floors = Floors(
            elevator=self.floors.elevator,
            f1=frozenset(new_1st_floor),
            f2=self.floors.f2,
            f3=self.floors.f3,
            f4=self.floors.f4,
            steps=self.floors.steps
        )
        best_floor = self.get_min_steps_to_top_floor(start_floors)

        best_floor.print()
        print()

        result = best_floor.steps

        print("Part 2:", result)

    @staticmethod
    def get_min_steps_to_top_floor(start_floors: Floors):
        queue: Queue = Queue()
        queue.put(start_floors)
        seen: Set[Floors] = set()
        seen.add(start_floors)

        best_floor = None
        while not queue.empty():
            if best_floor is not None:
                break

            floors: Floors = queue.get()

            for option in floors.options():
                if option not in seen:
                    if option.is_complete:
                        best_floor = option
                        break

                    seen.add(option)
                    queue.put(option)

        return best_floor


if __name__ == '__main__':
    code = Y2016D11("2016/11.txt")
    code.part1()
    code.part2()
