from __future__ import annotations
import re
from enum import Enum, auto
from typing import Dict

from aoc.util.inputs import Input


class OutType(Enum):
    Output = auto()
    Bot = auto()


class Bot(object):
    def __init__(self):
        self.values = []
        self.low_out_num = 0
        self.low_out_type = None
        self.high_out_num = 0
        self.high_out_type = None

    @property
    def empty(self):
        return len(self.values) == 0

    @property
    def ready_to_give(self):
        return len(self.values) == 2

    def give(self, bots: Dict[int, Bot], outputs: Dict[int, int]):
        low_value = min(self.values)
        high_value = max(self.values)
        self.values.remove(low_value)
        self.values.remove(high_value)

        if self.low_out_type == OutType.Bot:
            bots[self.low_out_num].values.append(low_value)
        else:
            outputs[self.low_out_num] = low_value

        if self.high_out_type == OutType.Bot:
            bots[self.high_out_num].values.append(high_value)
        else:
            outputs[self.high_out_num] = high_value


class Y2016D10(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()

        value_re = re.compile(r'value (\d+) goes to bot (\d+)')
        give_re = re.compile(r'bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)')

        self.bots = {}
        self.outputs = {}

        for line in lines:
            if (matched := give_re.match(line)) is not None:
                bot_id = int(matched.group(1))
                bot = self.bots.setdefault(bot_id, Bot())
                bot.low_out_type = OutType.Bot if matched.group(2) == "bot" else OutType.Output
                bot.low_out_num = int(matched.group(3))
                bot.high_out_type = OutType.Bot if matched.group(4) == "bot" else OutType.Output
                bot.high_out_num = int(matched.group(5))
            elif (matched := value_re.match(line)) is not None:
                bot_id = int(matched.group(2))
                bot = self.bots.setdefault(bot_id, Bot())
                bot.values.append(int(matched.group(1)))

        self.result_part_1 = None
        while True:
            if all(bot.empty for bot in self.bots.values()):
                break

            any_given = False
            for bot_id, bot in self.bots.items():
                if bot.ready_to_give:
                    if 17 in bot.values and 61 in bot.values:
                        self.result_part_1 = bot_id
                    bot.give(self.bots, self.outputs)
                    any_given = True
            if not any_given:
                raise ValueError("Nothing given!")

    def part1(self):
        result = self.result_part_1

        print("Part 1:", result)

    def part2(self):
        result = self.outputs[0] * self.outputs[1] * self.outputs[2]

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2016D10("2016/10.txt")
    code.part1()
    code.part2()
