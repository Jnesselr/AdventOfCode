from dataclasses import dataclass
from enum import Enum, auto

from aoc.util.inputs import Input
from aoc.util.queue import PriorityQueue


class Spell(Enum):
    MagicMissile = auto()
    Drain = auto()
    Shield = auto()
    Poison = auto()
    Recharge = auto()


class BattleState(object):
    mana_cost = {
        Spell.MagicMissile: 53,
        Spell.Drain: 73,
        Spell.Shield: 113,
        Spell.Poison: 173,
        Spell.Recharge: 229,
    }

    def __init__(self, boss_hp, boss_damage, hard_mode=False):
        self.my_mana = 500
        self.my_hp = 50
        self.my_armor = 0
        self.mana_spent = 0

        self.boss_hp = boss_hp
        self.boss_damage = boss_damage

        self.effects = {}
        self.castings = []
        self.hard_mode = hard_mode
        self._previous = None

    def copy(self):
        result = BattleState(self.boss_hp, self.boss_damage, self.hard_mode)
        result.my_mana = self.my_mana
        result.my_hp = self.my_hp
        result.my_armor = self.my_armor
        result.mana_spent = self.mana_spent
        result.effects = self.effects.copy()
        result.castings = self.castings.copy()
        result._previous = self

        return result

    def can_cast(self, spell: Spell):
        if self.mana_cost[spell] > self.my_mana:
            return False

        # at 1 turn remaining, it would end right before we cast it.
        if spell in self.effects and self.effects[spell] > 1:
            return False

        return True

    def cast(self, spell: Spell):
        result: BattleState = self.copy()
        if self.hard_mode:
            result.my_hp -= 1
            if result.my_hp == 0:
                return result

        # My turn
        result._apply_effects()

        result.mana_spent += self.mana_cost[spell]
        result.my_mana -= self.mana_cost[spell]
        result.castings.append(spell)

        if spell == Spell.MagicMissile:
            result.boss_hp = max(0, result.boss_hp - 4)
        elif spell == Spell.Drain:
            result.boss_hp = max(0, result.boss_hp - 2)
            result.my_hp += 2
        elif spell == Spell.Shield:
            result.effects[Spell.Shield] = 6
            result.my_armor += 7
        elif spell == Spell.Poison:
            result.effects[Spell.Poison] = 6
        elif spell == Spell.Recharge:
            result.effects[Spell.Recharge] = 5

        if result.boss_hp == 0:
            return result  # No boss turn, you're dead!

        # Boss Turn
        result._apply_effects()
        damage_to_me = max(1, result.boss_damage - result.my_armor)
        result.my_hp = max(0, result.my_hp - damage_to_me)

        return result

    def _apply_effects(self):
        for spell, turn_count in list(self.effects.items()):
            turn_count -= 1
            if spell == Spell.Shield:
                if turn_count == 0:
                    self.my_armor -= 7
            elif spell == Spell.Poison:
                self.boss_hp = max(0, self.boss_hp - 3)
            elif spell == Spell.Recharge:
                self.my_mana += 101

            if turn_count == 0:
                del self.effects[spell]
            else:
                self.effects[spell] = turn_count


class Y2015D22(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()

        self.boss_hp = 0
        self.boss_damage = 0

        for line in lines:
            if line.startswith("Hit Points"):
                self.boss_hp = int(line[12:])
            elif line.startswith("Damage"):
                self.boss_damage = int(line[8:])

    def part1(self):
        initial_battle_state = BattleState(self.boss_hp, self.boss_damage)
        result = self._fight(initial_battle_state)

        print("Part 1:", result)

    def part2(self):
        initial_battle_state = BattleState(self.boss_hp, self.boss_damage, hard_mode = True)
        result = self._fight(initial_battle_state)

        print("Part 2:", result)

    @staticmethod
    def _fight(initial_battle_state):
        queue: PriorityQueue[BattleState] = PriorityQueue[BattleState]()
        queue.push(initial_battle_state, 0)
        while not queue.empty:
            state: BattleState = queue.pop()

            if state.boss_hp == 0:
                return state.mana_spent

            for spell in Spell:
                if state.can_cast(spell):
                    new_state: BattleState = state.cast(spell)

                    if new_state.my_hp > 0:
                        queue.push(new_state, new_state.mana_spent)


if __name__ == '__main__':
    code = Y2015D22("2015/22.txt")
    code.part1()
    code.part2()
