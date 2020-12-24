from dataclasses import dataclass
from enum import Enum, auto
from functools import reduce
from typing import List

from aoc.util.coordinate import Coordinate
from aoc.util.grid import Grid
from aoc.util.inputs import Input
from aoc.util.search import BinarySearch


class FighterType(Enum):
    Elf = auto()
    Goblin = auto()


@dataclass
class Fighter(object):
    type: FighterType
    location: Coordinate
    hit_points: int
    attack_power: int

    @property
    def is_alive(self):
        return self.hit_points > 0

    def __repr__(self):
        return f"<{self.type.name} at {self.location} with {self.attack_power} atk, {self.hit_points} hp>"

    def attacked(self, attack_power):
        self.hit_points = max(0, self.hit_points - attack_power)


class Battle(object):
    def __init__(self, initial_grid: Grid[str]):
        self._initial_grid = initial_grid
        self.grid: Grid[str] = initial_grid.copy()
        self.elves: List[Fighter] = []
        self.goblins: List[Fighter] = []

        self.reset()

    @property
    def winner(self) -> FighterType:
        if any(x.is_alive for x in self.elves):
            return FighterType.Elf
        else:
            return FighterType.Goblin

    def reset(self):
        self.grid = self._initial_grid.copy()
        self.elves = []
        self.goblins = []

        for coordinate in self.grid.find('E'):
            self.elves.append(Fighter(
                type=FighterType.Elf,
                location=coordinate,
                hit_points=200,
                attack_power=3
            ))

        for coordinate in self.grid.find('G'):
            self.goblins.append(Fighter(
                type=FighterType.Goblin,
                location=coordinate,
                hit_points=200,
                attack_power=3
            ))

    def boost_elves(self, boost_amount):
        for elf in self.elves:
            elf.attack_power += boost_amount

    def run(self) -> int:
        completed_rounds = 0
        while True:
            all_fighters = self.elves + self.goblins
            all_fighters = [x for x in all_fighters if x.is_alive]
            fighters_ordered: List[Fighter] = sorted(all_fighters, key=lambda x: x.location)

            for fighter in fighters_ordered:
                if not fighter.is_alive:
                    continue

                if fighter.type == FighterType.Elf:
                    enemies = [goblin for goblin in self.goblins if goblin.is_alive]
                else:
                    enemies = [elf for elf in self.elves if elf.is_alive]

                if len(enemies) == 0:
                    remaining_units = self.elves + self.goblins
                    remaining_units = [x for x in remaining_units if x.is_alive]
                    hit_points_sum = sum(x.hit_points for x in remaining_units)
                    return completed_rounds * hit_points_sum

                # Move phase
                best_move = self._get_best_move(fighter, enemies)

                if best_move is not None:
                    self._move_to(fighter, best_move)

                # Attack phase
                self._attack(fighter, enemies)

            # self.grid.print()
            # print()
            completed_rounds += 1

    def _get_best_move(self, fighter, enemies):
        fighter_neighbors = fighter.location.neighbors()
        enemy_locations = set(e.location for e in enemies)

        if len(set(enemy_locations).intersection(set(fighter_neighbors))) > 0:
            return None  # Don't move, we're in range!

        in_range = reduce(lambda acc, cur: acc.union(set(cur.neighbors())), enemy_locations, set())
        can_get_to = self.grid.flood_map(fighter.location, '.')
        can_get_to = dict(t for t in can_get_to.items() if t[0] in in_range)

        if len(can_get_to) == 0:
            return None  # You're surrounded!
        min_steps_value = min(list(can_get_to.values()))
        nearest = dict((coord, steps) for coord, steps in can_get_to.items() if steps == min_steps_value)
        to_move_towards = min(list(nearest.keys()))

        flood_map_back = self.grid.flood_map(to_move_towards, '.')
        move_options = dict(t for t in flood_map_back.items() if t[0] in fighter_neighbors)

        min_steps_value = min(list(move_options.values()))
        best_moves = set(coord for coord, steps in move_options.items() if steps == min_steps_value)
        best_move = min(best_moves)

        return best_move

    def _move_to(self, fighter: Fighter, best_move: Coordinate):
        old_value = self.grid[fighter.location]
        self.grid[fighter.location] = '.'
        fighter.location = best_move

        self.grid[best_move] = old_value

    def _attack(self, fighter: Fighter, enemies: List[Fighter]):
        neighbors = fighter.location.neighbors()

        enemies_in_range = [e for e in enemies if e.location in neighbors]
        if len(enemies_in_range) == 0:
            return

        fewest_hit_points = min(e.hit_points for e in enemies_in_range)
        enemies_can_attack = [e for e in enemies_in_range if e.hit_points == fewest_hit_points]
        attacked_enemy: Fighter = min(enemies_can_attack, key=lambda e: e.location)

        attacked_enemy.attacked(fighter.attack_power)

        if not attacked_enemy.is_alive:
            self.grid[attacked_enemy.location] = '.'


class Y2018D15(object):
    def __init__(self, file_name):
        initial_grid = Input(file_name).grid()
        self.battle = Battle(initial_grid)

    def part1(self):
        result = self.battle.run()

        print("Part 1:", result)

    def part2(self):
        outcomes = {}

        def _elves_won(boost_value) -> bool:
            self.battle.reset()
            self.battle.boost_elves(boost_value)
            outcomes[boost_value + 3] = self.battle.run()

            elves_won = self.battle.winner == FighterType.Elf and \
                        all(x.is_alive for x in self.battle.elves)  # No elf left behind
            return elves_won

        elves_win = BinarySearch(_elves_won)
        boost_needed = elves_win.earliest(1, lambda x: 3 * x) + 3
        print(boost_needed)
        result = outcomes[boost_needed]

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2018D15("2018/15.txt")
    code.part1()
    code.part2()
