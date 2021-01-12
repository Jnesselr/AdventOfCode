import re
from typing import Dict

from aoc.util.inputs import Input
from aoc.util.tasks import Tasking


def w(state, value):
    return state[value] if value.isalpha() else int(value)


class Y2015D7(object):
    assignment_regex = re.compile(r'(\w+|\d+) -> (\w+)')
    not_regex = re.compile(r'NOT (\w+|\d+) -> (\w+)')
    and_regex = re.compile(r'(\w+|\d+) AND (\w+|\d+) -> (\w+)')
    or_regex = re.compile(r'(\w+|\d+) OR (\w+|\d+) -> (\w+)')
    lshift_regex = re.compile(r'(\w+|\d+) LSHIFT (\d+) -> (\w+)')
    rshift_regex = re.compile(r'(\w+|\d+) RSHIFT (\d+) -> (\w+)')

    def __init__(self, file_name):
        lines = Input(file_name).lines()

        self.tasks: Tasking[str] = Tasking[str]()
        self.operations = {}
        self.arguments = {}

        for line in lines:
            if matched := self.assignment_regex.match(line):
                value, output = matched.groups()
                if value.isalpha():
                    self.tasks.requires(output, value)
                self.arguments[output] = (value,)

                self.operations[matched.group(2)] = lambda state, x: w(state, x)
            elif matched := self.not_regex.match(line):
                left, output = matched.groups()
                if left.isalpha():
                    self.tasks.requires(output, left)
                self.arguments[output] = (left,)

                self.operations[output] = lambda state, x: 65535 - w(state, x)
            elif matched := self.and_regex.match(line):
                left, right, output = matched.groups()
                if left.isalpha():
                    self.tasks.requires(output, left)
                if right.isalpha():
                    self.tasks.requires(output, right)
                self.arguments[output] = left, right

                self.operations[output] = lambda state, x, y: w(state, x) & w(state, y)
            elif matched := self.or_regex.match(line):
                left, right, output = matched.groups()
                if left.isalpha():
                    self.tasks.requires(output, left)
                if right.isalpha():
                    self.tasks.requires(output, right)
                self.arguments[output] = left, right

                self.operations[output] = lambda state, x, y: w(state, x) | w(state, y)
            elif matched := self.lshift_regex.match(line):
                left, right, output = matched.groups()
                if left.isalpha():
                    self.tasks.requires(output, left)
                if right.isalpha():
                    self.tasks.requires(output, right)
                self.arguments[output] = left, right

                self.operations[output] = lambda state, x, y: (w(state, x) << int(y)) & 65535
            elif matched := self.rshift_regex.match(line):
                left, right, output = matched.groups()
                if left.isalpha():
                    self.tasks.requires(output, left)
                if right.isalpha():
                    self.tasks.requires(output, right)
                self.arguments[output] = left, right

                self.operations[output] = lambda state, x, y: (w(state, x) >> int(y)) & 65535
            else:
                raise ValueError(f"Could not parse: {line}")

    def part1(self):
        state = self._compute_wires({})
        result = state['a']

        print("Part 1:", result)

    def part2(self):
        state = self._compute_wires({})
        state = self._compute_wires({'b': state['a']})
        result = state['a']

        print("Part 2:", result)

    def _compute_wires(self, initial_state: Dict[str, int]) -> Dict[str, int]:
        state: Dict[str, int] = initial_state.copy()

        tasking = self.tasks.copy()

        while len(tasks := tasking.available_tasks) > 0:
            for task in tasks:
                if task not in state:
                    state[task] = self.operations[task](state, *self.arguments[task])

                tasking.done(task)

        return state


if __name__ == '__main__':
    code = Y2015D7("2015/7.txt")
    code.part1()
    code.part2()
