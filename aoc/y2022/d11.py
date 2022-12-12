import re
from collections import Counter
from dataclasses import dataclass, field
from math import prod
from queue import Queue
from typing import Callable, List

from aoc.util.inputs import Input


@dataclass
class Monkey:
    id: int
    operation: Callable[[int], int]
    test_divisible: int
    true_monkey: int
    false_monkey: int
    items: Queue = field(default_factory=lambda: Queue())

    @staticmethod
    def from_group(m_group: List[str]):
        _id = int(re.match(r'Monkey (\d+):', m_group[0]).group(1))
        _starting_items = [int(x) for x in re.match(r'\s+Starting items: (.*)', m_group[1]).group(1).split(',')]
        _operation_match = re.match(r'\s+Operation: new = old ([+*]) (.*)', m_group[2])
        _test_divisible = int(re.match(r'\s+Test: divisible by (\d+)', m_group[3]).group(1))
        _true_monkey = int(re.match(r'\s+ If true: throw to monkey (\d+)', m_group[4]).group(1))
        _false_monkey = int(re.match(r'\s+ If false: throw to monkey (\d+)', m_group[5]).group(1))

        op = None
        if _operation_match.group(2) == 'old':
            if _operation_match.group(1) == '+':
                op = lambda x: x + x
            elif _operation_match.group(1) == '*':
                op = lambda x: x * x
        else:
            if _operation_match.group(1) == '+':
                op = lambda x: x + int(_operation_match.group(2))
            elif _operation_match.group(1) == '*':
                op = lambda x: x * int(_operation_match.group(2))

        monkey = Monkey(
            id=_id,
            operation=op,
            test_divisible=_test_divisible,
            true_monkey=_true_monkey,
            false_monkey=_false_monkey
        )

        for item in _starting_items:
            monkey.items.put(item)

        return monkey


def debug(*args, **kwargs):
    if False:
        print(*args, **kwargs)


def end_round(*args, **kwargs):
    if False:
        print(*args, **kwargs)


class Y2022D11(object):
    def __init__(self, file_name):
        self.groups = Input(file_name).grouped()

    def dance_monkey_dance(self, rounds: int, divide_by_3: bool) -> int:
        monkeys = [Monkey.from_group(g) for g in self.groups]
        global_div = prod([m.test_divisible for m in monkeys])
        inspection_count = Counter()

        for _ in range(rounds):  # 20 rounds
            for monkey in monkeys:
                debug(f"Monkey {monkey.id}")
                while not monkey.items.empty():
                    inspection_count[monkey.id] += 1
                    item = monkey.items.get()
                    new_item = monkey.operation(item)
                    debug(f"  Monkey inspects an item with a worry level of {item}")
                    debug(f"    Worry level {item} -> {new_item}")
                    new_item = new_item % global_div
                    if divide_by_3:
                        new_item = new_item // 3
                    debug(f"    Monkey gets bored with item. Worry level is divided by 3 to {new_item}")

                    if new_item % monkey.test_divisible == 0:
                        debug(f"    Current worry level is divisible by {monkey.test_divisible}")
                        debug(f"    Item with worry level {new_item} is thrown to monkey {monkey.true_monkey}.")
                        monkeys[monkey.true_monkey].items.put(new_item)
                    else:
                        debug(f"    Current worry level is not divisible by {monkey.test_divisible}")
                        debug(f"    Item with worry level {new_item} is thrown to monkey {monkey.false_monkey}.")
                        monkeys[monkey.false_monkey].items.put(new_item)

            for monkey in monkeys:
                item_list = ', '.join([str(x) for x in list(monkey.items.queue)])
                end_round(f"Monkey {monkey.id}: {item_list}")

        if False:
            for monkey in monkeys:
                print(f"Monkey {monkey.id} inspected items {inspection_count[monkey.id]} times.")

        return prod([x[1] for x in inspection_count.most_common(2)])

    def part1(self):
        result = self.dance_monkey_dance(rounds=20, divide_by_3=True)

        print("Part 1:", result)

    def part2(self):
        result = self.dance_monkey_dance(rounds=10_000, divide_by_3=False)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2022D11("2022/11.txt")
    code.part1()
    code.part2()
