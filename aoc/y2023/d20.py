import enum
import math
import re
from collections import defaultdict
from dataclasses import dataclass
from queue import Queue

from aoc.util.graph import Graph
from aoc.util.inputs import Input


class ModuleType(enum.Enum):
    UNTYPED = enum.auto()
    FLIP_FLOP = enum.auto()
    CONJUNCTION = enum.auto()
    BROADCASTER = enum.auto()


@dataclass(frozen=True)
class PulseType:
    incoming_from: str
    going_to: str
    is_high: bool


class Machine:
    def __init__(self, lines):
        self._lines = lines
        self._types: dict[str, ModuleType] = {}
        self._notify: defaultdict[str, list[str]] = defaultdict(lambda: [])
        self._inputs: defaultdict[str, list[str]] = defaultdict(lambda: [])  # Order does not matter

        line_re = re.compile(r'([%&]?)(\w+) -> (.*)')
        for line in lines:
            match = line_re.match(line)
            name = match.group(2)
            module_type = match.group(1)
            if module_type == '':
                self._types[name] = ModuleType.BROADCASTER  # Only the broadcaster has no type on the left
            elif module_type == '%':
                self._types[name] = ModuleType.FLIP_FLOP
            elif module_type == '&':
                self._types[name] = ModuleType.CONJUNCTION

            for outgoing in match.group(3).split(', '):
                self._types.setdefault(outgoing, ModuleType.UNTYPED)
                self._notify[name].append(outgoing)
                self._inputs[outgoing].append(name)

        self._states: dict[str, bool] = {k: False for k in self._types.keys()}  # False is low
        self._conjunctions: dict[str, dict[str, bool]] = {
            c_key: {i_key: False for i_key in self._inputs[c_key]}
            for c_key, c_type in self._types.items() if c_type == ModuleType.CONJUNCTION
        }

        self.sr_time = 0  # 3923
        self.sn_time = 0  # 3967
        self.rf_time = 0  # 4021
        self.vq_time = 0  # 3917
        self._presses = 0

    def get_rx_timing(self) -> int:
        return math.lcm(self.sr_time, self.sn_time, self.rf_time, self.vq_time)

    def press_button(self, num_times: int) -> int:
        low_pulse = 0
        high_pulse = 0
        for button_press in range(num_times):
            l, h = self.press_button_once()
            low_pulse += l
            high_pulse += h

        return low_pulse * high_pulse

    def press_button_once(self) -> tuple[int, int]:
        low_pulse = 0
        high_pulse = 0
        self._presses += 1

        q = Queue()
        initial_pulse: PulseType = PulseType(incoming_from="button", going_to="broadcaster", is_high=False)
        q.put(initial_pulse)
        while not q.empty():
            pulse: PulseType = q.get()
            # print(pulse)
            incoming_from: str = pulse.incoming_from
            going_to: str = pulse.going_to
            is_high: bool = pulse.is_high

            if incoming_from == 'sr' and is_high and self.sr_time == 0:
                self.sr_time = self._presses
            if incoming_from == 'sn' and is_high and self.sn_time == 0:
                self.sn_time = self._presses
            if incoming_from == 'rf' and is_high and self.rf_time == 0:
                self.rf_time = self._presses
            if incoming_from == 'vq' and is_high and self.vq_time == 0:
                self.vq_time = self._presses

            if is_high:
                high_pulse += 1
            else:
                low_pulse += 1

            current_state: bool = self._states[going_to]
            module_type: ModuleType = self._types[going_to]

            if module_type == ModuleType.UNTYPED:
                continue  # Nothing to do here
            elif module_type == ModuleType.FLIP_FLOP:
                if not is_high:  # If incoming pulse is low
                    self._states[going_to] = current_state = not current_state  # Invert state
                    for outgoing in self._notify[going_to]:
                        q.put(PulseType(
                            incoming_from=going_to,
                            going_to=outgoing,
                            is_high=current_state
                        ))
            elif module_type == ModuleType.CONJUNCTION:
                self._conjunctions[going_to][incoming_from] = is_high
                output_high = True
                if all(self._conjunctions[going_to][incoming] for incoming in self._conjunctions[going_to].keys()):
                    output_high = False

                for outgoing in self._notify[going_to]:
                    q.put(PulseType(
                        incoming_from=going_to,
                        going_to=outgoing,
                        is_high=output_high
                    ))
            elif module_type == ModuleType.BROADCASTER:
                for outgoing in self._notify[going_to]:
                    q.put(PulseType(
                        incoming_from=going_to,
                        going_to=outgoing,
                        is_high=False
                    ))
        return low_pulse, high_pulse


class Y2023D20(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.machine = Machine(lines)

    def part1(self):
        result = self.machine.press_button(1000)

        print("Part 1:", result)

    def part2(self):
        result = 0
        while result == 0:
            self.machine.press_button_once()
            result = self.machine.get_rx_timing()

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2023D20("2023/20.txt")
    code.part1()
    code.part2()
