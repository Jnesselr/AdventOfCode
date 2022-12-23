import re
from dataclasses import dataclass, field
from queue import Queue
from typing import Optional

from z3 import Solver, Int, ArithRef, Const, IntVal

from aoc.util.inputs import Input


@dataclass
class Monkey:
    name: str
    value: Optional[int] = field(default=None)
    operation: Optional[str] = field(default=None)
    left: Optional['Monkey'] = field(default=None)
    right: Optional['Monkey'] = field(default=None)

    def fill_values(self):
        if self.value is not None:
            return

        self.left.fill_values()
        self.right.fill_values()

        left_value = self.left.value
        right_value = self.right.value
        magic_method = {
            '+': int.__add__,
            '-': int.__sub__,
            '*': int.__mul__,
            '/': int.__floordiv__,
        }[self.operation]
        self.value = magic_method(left_value, right_value)

    def has_monkey(self, name: str) -> bool:
        if self.name == name:
            return True

        has_name = False
        if self.left is not None:
            has_name |= self.left.has_monkey(name)

        if self.right is not None:
            has_name |= self.right.has_monkey(name)

        return has_name

    def int_ref(self) -> ArithRef:
        if self.name == 'humn':
            return Int('humn')

        if self.left is None and self.right is None:  # Don't trust the filled values at this point
            return IntVal(self.value)

        if self.operation == '+':
            return self.left.int_ref() + self.right.int_ref()
        elif self.operation == '-':
            return self.left.int_ref() - self.right.int_ref()
        elif self.operation == '*':
            return self.left.int_ref() * self.right.int_ref()
        elif self.operation == '/':
            return self.left.int_ref() / self.right.int_ref()


class Y2022D21(object):
    number_regex = re.compile(r'(\w+): (\d+)')
    operation_regex = re.compile(r'(\w+): (\w+) ([+\-*/]) (\w+)')

    def __init__(self, file_name):
        lines = Input(file_name).lines()

        monkeys = {}

        q = Queue()
        for line in lines:
            q.put(line)

        while not q.empty():
            line = q.get()
            if match := self.number_regex.match(line):
                name = match.group(1)
                monkeys[name] = Monkey(
                    name=name,
                    value=int(match.group(2)),
                )
            elif match := self.operation_regex.match(line):
                name, left, operation, right = match.groups()
                if left not in monkeys or right not in monkeys:
                    q.put(line)  # Can't process this yet, don't have dependencies
                    continue
                monkeys[name] = Monkey(
                    name=name,
                    operation=operation,
                    left=monkeys[left],
                    right=monkeys[right],
                )
            else:
                print(f"Match failed: {line}")

        self.root = monkeys['root']
        self.root.fill_values()

    def part1(self):
        result = self.root.value

        print("Part 1:", result)

    def part2(self):
        left = self.root.left
        right = self.root.right

        solver = Solver()

        solver.add(left.int_ref() == right.int_ref())
        solver.check()
        model = solver.model()
        # Get the humn variable declaration and cast it to a long. I don't know how to do that with the string humn.
        result = model[model.decls()[0]].as_long()

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2022D21("2022/21.txt")
    code.part1()
    code.part2()
