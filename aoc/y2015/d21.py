import itertools
from dataclasses import dataclass

from aoc.util.inputs import Input


@dataclass(frozen=True)
class ShopItem(object):
    cost: int
    damage: int
    armor: int


class BossFight(object):
    def __init__(self, hp, damage, armor):
        self.hp = hp
        self.damage = damage
        self.armor = armor

    def fight(self, my_hp, my_damage, my_armor):
        my_turn = True
        boss_hp = self.hp
        boss_damage = self.damage
        boss_armor = self.armor

        while boss_hp > 0 and my_hp > 0:
            if my_turn:
                damage = max(1, my_damage - boss_armor)
                boss_hp -= damage
            else:
                damage = max(1, boss_damage - my_armor)
                my_hp -= damage
            my_turn = not my_turn

        return my_hp


class Y2015D21(object):
    shop_weapons = {
        "Dagger": ShopItem(8, 4, 0),
        "Shortsword": ShopItem(10, 5, 0),
        "Warhammer": ShopItem(25, 6, 0),
        "Longsword": ShopItem(40, 7, 0),
        "Greataxe": ShopItem(74, 8, 0),
    }

    shop_armor = {
        "naked": ShopItem(0, 0, 0),
        "Leather": ShopItem(13, 0, 1),
        "Chainmail": ShopItem(31, 0, 2),
        "Splintmail": ShopItem(53, 0, 3),
        "Bandemail": ShopItem(75, 0, 4),
        "Platemail": ShopItem(102, 0, 5),
    }

    shop_rings = {
        "no_left": ShopItem(0, 0, 0),
        "no_right": ShopItem(0, 0, 0),
        "Damage +1": ShopItem(25, 1, 0),
        "Damage +2": ShopItem(50, 2, 0),
        "Damage +3": ShopItem(100, 3, 0),
        "Defense +1": ShopItem(20, 0, 1),
        "Defense +2": ShopItem(40, 0, 2),
        "Defense +3": ShopItem(80, 0, 3),
    }

    def __init__(self, file_name):
        lines = Input(file_name).lines()

        hit_points = 0
        damage = 0
        armor = 0

        for line in lines:
            if line.startswith("Hit Points"):
                hit_points = int(line[12:])
            elif line.startswith("Damage"):
                damage = int(line[8:])
            elif line.startswith("Armor"):
                armor = int(line[7:])

        boss_fight = BossFight(hit_points, damage, armor)

        self.best_gold = 1000
        self.worst_gold = 0

        for weapon_item in self.shop_weapons.values():
            for armor_item in self.shop_armor.values():
                for left_ring, right_ring in itertools.combinations(self.shop_rings.values(), r=2):
                    cost = weapon_item.cost + armor_item.cost + left_ring.cost + right_ring.cost
                    my_hp = 100
                    my_damage = weapon_item.damage + armor_item.damage + left_ring.damage + right_ring.damage
                    my_armor = weapon_item.armor + armor_item.armor + left_ring.armor + right_ring.armor

                    fight_result = boss_fight.fight(my_hp, my_damage, my_armor)

                    if fight_result > 0:
                        self.best_gold = min(self.best_gold, cost)
                    else:
                        self.worst_gold = max(self.worst_gold, cost)

    def part1(self):
        result = self.best_gold

        print("Part 1:", result)

    def part2(self):
        result = self.worst_gold

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2015D21("2015/21.txt")
    code.part1()
    code.part2()
