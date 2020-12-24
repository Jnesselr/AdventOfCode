from __future__ import annotations
import re
import uuid
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict, Optional

from aoc.util.inputs import Input
from aoc.util.search import BinarySearch


class GroupType(Enum):
    ImmuneSystem = auto()
    Infection = auto()


@dataclass
class Group(object):
    type: GroupType
    unit_count: int
    hit_points: int
    weaknesses: List[str]
    immunities: List[str]
    attack_damage: int
    damage_type: str
    initiative: int
    id: str = field(default_factory=lambda: uuid.uuid4().hex)

    @property
    def is_alive(self):
        return self.unit_count > 0

    @property
    def effective_power(self):
        return self.unit_count * self.attack_damage

    def damage_amount(self, other: Group):
        if self.damage_type in other.immunities:
            return 0

        if self.damage_type in other.weaknesses:
            return 2 * self.effective_power

        return self.effective_power

    def attacked_by(self, other: Group):
        units_lost = other.damage_amount(self) // self.hit_points
        self.unit_count = max(0, self.unit_count - units_lost)


class Combat(object):
    def __init__(self, groups):
        self._groups = groups
        self.immune_system = []
        self.infection = []
        self.fighter_map = {}
        self.reset()

    def reset(self):
        self.immune_system = self._parse(self._groups[0][1:], GroupType.ImmuneSystem)
        self.infection = self._parse(self._groups[1][1:], GroupType.Infection)

        self.fighter_map = {}
        fighter: Group
        for fighter in self.immune_system:
            self.fighter_map[fighter.id] = fighter

        fighter: Group
        for fighter in self.infection:
            self.fighter_map[fighter.id] = fighter

    @staticmethod
    def _parse(lines, _type: GroupType) -> List[Group]:
        result = []
        for line in lines:
            matched = re.match(
                r'(\d+) units each with (\d+) hit points (.*)'
                r'with an attack that does (\d+) (\w+) damage at initiative (\d+)',
                line
            )
            weaknesses = []
            immunities = []

            specialties = matched.group(3)
            if len(specialties) > 0:
                for specialty in specialties[1:-2].split("; "):
                    if specialty.startswith("weak to"):
                        weaknesses = specialty[8:].split(", ")
                    elif specialty.startswith("immune to"):
                        immunities = specialty[10:].split(", ")

            result.append(Group(
                type=_type,
                unit_count=int(matched.group(1)),
                hit_points=int(matched.group(2)),
                weaknesses=weaknesses,
                immunities=immunities,
                attack_damage=int(matched.group(4)),
                damage_type=matched.group(5),
                initiative=int(matched.group(6))
            ))

        return result

    @property
    def remaining_units(self):
        result = sum(x.unit_count for x in self.immune_system if x.is_alive)
        result += sum(x.unit_count for x in self.infection if x.is_alive)
        return result

    @property
    def winner(self) -> Optional[GroupType]:
        if any(x.is_alive for x in self.immune_system):
            return GroupType.ImmuneSystem
        elif any(x.is_alive for x in self.immune_system):
            return GroupType.Infection
        else:
            return None

    def boost_immunity(self, amount):
        for fighter in self.immune_system:
            fighter.attack_damage += amount

    def war(self):
        while True:
            immune_system_alive = any(True for x in self.immune_system if x.is_alive)
            infection_alive = any(True for x in self.infection if x.is_alive)

            if not immune_system_alive or not infection_alive:
                break

            self.fight()

    def fight(self):
        all_fighters: List[Group] = self.immune_system + self.infection
        all_fighters = [x for x in all_fighters if x.is_alive]

        all_fighters = sorted(all_fighters, key=lambda x: (-x.effective_power, -x.initiative))
        matchings = self._pick_targets(all_fighters)

        all_fighters = sorted(all_fighters, key=lambda x: -x.initiative)

        units_killed = 0
        for fighter in all_fighters:
            if not fighter.is_alive:
                continue

            if fighter.id not in matchings:
                continue

            opponent: Group = self.fighter_map[matchings[fighter.id]]
            previous_units = opponent.unit_count
            opponent.attacked_by(fighter)
            units_killed += (opponent.unit_count - previous_units)

        if units_killed == 0:
            # No damage was dealt, kill them all to avoid an infinite loop.
            for fighter in all_fighters:
                fighter.unit_count = 0

    @staticmethod
    def _pick_targets(all_fighters: List[Group]) -> Dict[str, str]:
        fight_matching: Dict[str, str] = {}

        for fighter in all_fighters:
            best_targets = sorted([
                target for target in all_fighters
                if target.is_alive and target.type != fighter.type and target.id not in fight_matching.values()
            ],
                key=lambda target: (-fighter.damage_amount(target), -target.effective_power, -target.initiative)
            )

            if len(best_targets) == 0:
                continue

            best_target = best_targets[0]

            if fighter.damage_amount(best_target) == 0:
                continue

            fight_matching[fighter.id] = best_target.id

        return fight_matching


class Y2018D24(object):
    def __init__(self, file_name):
        groups = Input(file_name).grouped()
        self.combat = Combat(groups)

    def part1(self):
        self.combat.reset()
        self.combat.war()
        result = self.combat.remaining_units

        print("Part 1:", result)

    def part2(self):
        outcomes = {}

        def _immunity_wins(boost_value) -> bool:
            self.combat.reset()
            self.combat.boost_immunity(boost_value)
            self.combat.war()
            outcomes[boost_value] = self.combat.remaining_units

            return self.combat.winner == GroupType.ImmuneSystem

        search = BinarySearch(_immunity_wins)
        smallest_boost = search.earliest(1, lambda x: 8 * x)

        result = outcomes[smallest_boost]

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2018D24("2018/24.txt")
    code.part1()
    code.part2()
