import re
from dataclasses import dataclass

from aoc.util.inputs import Input


@dataclass(frozen=True)
class Action(object):
    value: int
    cursor_change: int
    new_state: str


class TuringMachine(object):
    def __init__(self, starting_state: str):
        self.state = starting_state
        self.tape = {}
        self.cursor = 0

        # State -> current value -> action
        self._actions = {}

    def add_action(self, state: str, zero_action: Action, one_action: Action):
        self._actions.setdefault(state, {})
        self._actions[state][0] = zero_action
        self._actions[state][1] = one_action

    def step(self):
        current_value = self.tape.setdefault(self.cursor, 0)
        action = self._actions[self.state][current_value]
        self.tape[self.cursor] = action.value
        self.cursor += action.cursor_change
        self.state = action.new_state

    @property
    def checksum(self):
        return sum(1 for value in self.tape.values() if value == 1)


class Y2017D25(object):

    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.machine = None
        self.diagnostic_checksum_steps = 0

        begin_state_re = re.compile(r'Begin in state (\w+)')
        diagnostic_checksum_re = re.compile(r'Perform a diagnostic checksum after (\d+) steps.')
        in_state_re = re.compile(r'In state (\w+):')
        current_value_re = re.compile(r'\s+If the current value is (\d+):')
        write_value_re = re.compile(r'\s+- Write the value (\d+).')
        move_slot_re = re.compile(r'\s+- Move one slot to the (\w+).')
        continue_state_re = re.compile(r'\s+- Continue with state (\w+).')

        current_state = None
        current_value = None
        new_value = None
        cursor_change = None
        new_state = None
        actions = {}
        for line in lines:
            if (matched := begin_state_re.match(line)) is not None:
                self.machine = TuringMachine(matched.group(1))
            elif (matched := diagnostic_checksum_re.match(line)) is not None:
                self.diagnostic_checksum_steps = int(matched.group(1))
            elif (matched := in_state_re.match(line)) is not None:
                current_state = matched.group(1)
            elif (matched := current_value_re.match(line)) is not None:
                current_value = int(matched.group(1))
            elif (matched := write_value_re.match(line)) is not None:
                new_value = int(matched.group(1))
            elif (matched := move_slot_re.match(line)) is not None:
                cursor_change = 1 if matched.group(1) == "right" else -1
            elif (matched := continue_state_re.match(line)) is not None:
                new_state = matched.group(1)
            elif line == '':
                pass
            else:
                raise ValueError(line)

            if current_value is not None and \
                    new_value is not None and \
                    cursor_change is not None and \
                    new_state is not None:
                actions[current_value] = Action(
                    value=new_value,
                    cursor_change=cursor_change,
                    new_state=new_state
                )

                current_value = None
                new_value = None
                cursor_change = None
                new_state = None

            if 0 in actions and 1 in actions:
                self.machine.add_action(current_state, actions[0], actions[1])
                current_state = None
                actions = {}

    def part1(self):
        for i in range(self.diagnostic_checksum_steps):
            self.machine.step()

        result = self.machine.checksum

        print("Part 1:", result)

    def part2(self):
        pass


if __name__ == '__main__':
    code = Y2017D25("2017/25.txt")
    code.part1()
    code.part2()
