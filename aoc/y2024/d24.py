import abc
import re
from abc import ABC
from collections import defaultdict
from copy import copy
from functools import cached_property
from itertools import combinations
from queue import Queue
from typing import Optional

from aoc.util.inputs import Input


class Bit(abc.ABC):
    def __init__(self, value: bool, name: Optional[str] = None):
        self._value: bool = value
        self._name: Optional[str] = name
        self.children: set[BinaryGate] = set()

    @property
    def value(self) -> bool:
        return self._value

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    def __hash__(self):
        if isinstance(self, In):
            return hash(self.name)
        if isinstance(self, BinaryGate):
            return hash(self.left) + hash(self.right)
        raise Exception("not hashable")

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if isinstance(self, BinaryGate) and isinstance(other, BinaryGate):
            if self.left != other.left and self.left != other.right:
                return False
            if self.right != other.left and self.right != other.right:
                return False
        return self._name == other._name

    def __and__(self, other: 'Bit') -> 'Bit':
        and_gate = AndGate(self, other)

        if isinstance(self, Constant) and isinstance(other, Constant):
            return Constant(and_gate.value)
        if isinstance(self, Constant):
            # 1 & a -> a
            # 0 & a -> 0
            return other if self.value else Constant(False)
        if isinstance(other, Constant):
            # a & 1 -> a
            # a & 0 -> 0
            return self if other.value else Constant(False)

        self.children.add(and_gate)
        other.children.add(and_gate)

        return and_gate

    def __or__(self, other: 'Bit') -> 'Bit':
        or_gate = OrGate(self, other)

        if isinstance(self, Constant) and isinstance(other, Constant):
            return Constant(or_gate.value)
        if isinstance(self, Constant):
            # 1 | a -> 1
            # 0 | a -> a
            return Constant(True) if self.value else other
        if isinstance(other, Constant):
            # a | 1 -> 1
            # a | 0 -> a
            return Constant(True) if other.value else self

        self.children.add(or_gate)
        other.children.add(or_gate)

        return or_gate

    def __xor__(self, other: 'Bit') -> 'Bit':
        xor_gate = XorGate(self, other)

        if isinstance(self, Constant) and isinstance(other, Constant):
            return Constant(xor_gate.value)
        if isinstance(self, Constant) and not self.value:
            return other  # 0 ^ a -> a
        if isinstance(other, Constant) and not other.value:
            return self  # a ^ 0 -> a

        # We could simplify the xor gate more if we were willing to use a not gate... but we're not.
        self.children.add(xor_gate)
        other.children.add(xor_gate)

        return xor_gate

    @abc.abstractmethod
    def _calculate(self) -> None:
        pass


class Constant(Bit):
    def __init__(self, value: bool):
        name = "const1" if value else "const0"
        super().__init__(value, name)

    def __eq__(self, other):
        if not isinstance(other, Constant):
            return False
        return self.value == other.value

    def _calculate(self) -> None:
        pass


class In(Bit):
    def __init__(self, name: str, initial_value: bool = False):
        super().__init__(initial_value, name)

    @Bit.value.setter
    def value(self, value: bool):
        self._value = value
        for child in self.children:
            child._calculate()

    def _calculate(self) -> None:
        pass


class BinaryGate(Bit, ABC):
    def __init__(self, left: Bit, right: Bit, name: Optional[str] = None):
        self.left = left
        self.right = right
        super().__init__(False, name)
        self._calculate()


class AndGate(BinaryGate):
    def _calculate(self):
        self._value = self.left.value and self.right.value
        for child in self.children:
            child._calculate()


class OrGate(BinaryGate):
    def _calculate(self):
        self._value = self.left.value or self.right.value
        for child in self.children:
            child._calculate()


class XorGate(BinaryGate):
    def _calculate(self):
        self._value = self.left.value != self.right.value
        for child in self.children:
            child._calculate()


class AdderLoopException(Exception):
    pass


class BadAdder:
    _input_re = re.compile(r'(\w+): ([01])')
    _combining_re = re.compile(r'(\w+) (AND|OR|XOR) (\w+) -> (\w+)')

    def __init__(self, lines: list[str], swaps: Optional[set[tuple[str, str]]] = None):
        self._lines = lines

        if swaps is None:
            swaps = set()

        self._swaps = swaps

        self._input_states: dict[str, In] = {}

        q = Queue()
        for line in lines:
            if line == "":
                continue
            elif (match := self._input_re.match(line)) is not None:
                name, bit_value = match.groups()
                self._input_states[name] = In(name, True if bit_value == '1' else False)
            elif (match := self._combining_re.match(line)) is not None:
                q.put(match.groups())

        states: dict[str, Bit] = dict(self._input_states)
        swap_map = {}
        for swap in swaps:
            swap_map[swap[0]] = swap[1]
            swap_map[swap[1]] = swap[0]

        self._z_bits = {}
        same_counter = 0
        while not q.empty():
            match = q.get()
            left, comb, right, out = match
            if left not in states or right not in states:
                q.put(match)
                same_counter += 1
                if same_counter >= q.qsize():
                    raise AdderLoopException("Looped all the way back around")
                continue

            same_counter = 0

            if out in swap_map:
                out = swap_map[out]

            if comb == "AND":
                states[out] = states[left] & states[right]
            elif comb == "OR":
                states[out] = states[left] | states[right]
            elif comb == "XOR":
                states[out] = states[left] ^ states[right]
            else:
                raise Exception("Unknown gate type")
            states[out].name = out

            if out.startswith('z'):
                self._z_bits[out] = states[out]

        self._result = 0
        for i, z_name in enumerate(sorted(self._z_bits.keys())):
            self._result |= (1 if self._z_bits[z_name].value else 0) << i

    @cached_property
    def max_input(self) -> int:
        return max([
            int(i.replace('x', '').replace('y', ''))
            for i in self._input_states.keys()
        ])

    def x(self, i: int) -> Bit:
        return self._input_states[f"x{i:02}"]

    def y(self, i: int) -> Bit:
        return self._input_states[f"y{i:02}"]

    def z(self, i: int) -> Bit:
        return self._input_states[f"z{i:02}"]

    @cached_property
    def result(self) -> int:
        return self._result

    def with_swaps(self, swappable: frozenset[tuple[str, str]]) -> 'BadAdder':
        return BadAdder(
            self._lines,
            self._swaps.union(swappable)
        )

    def find_mismatch(self, *outputs: BinaryGate) -> Optional[tuple[str, str]]:
        name_to_bit, working_pairs = self.__names_and_working_pairs(*outputs)
        _, bad_pairs = self.__names_and_working_pairs(*self._z_bits.values())

        name_queue = Queue()
        seen_names = set()
        for name in name_to_bit.keys():
            name_queue.put(name)
            seen_names.add(name)

        while not name_queue.empty():
            name: str = name_queue.get()
            valid_pairings = {t: v for t, v in working_pairs.items() if t[0] == name}

            for bit_pair, gates in valid_pairings.items():
                bit_pair_inverse: tuple[str, str] = bit_pair[1], bit_pair[0]
                if bit_pair in bad_pairs:
                    bad_gates = bad_pairs[bit_pair]
                elif bit_pair_inverse in bad_pairs:
                    bad_gates = bad_pairs[bit_pair_inverse]
                else:
                    bad_gates = []

                for gate in gates:
                    if gate.name is not None:
                        continue
                    limited_gates = [g for g in bad_gates if type(g) == type(gate)]
                    if len(limited_gates) != 1:
                        return bit_pair

                    gate.name = limited_gates[0].name
                    name_to_bit[gate.name] = gate

                    if gate.name not in seen_names:
                        seen_names.add(gate.name)
                        name_queue.put(gate.name)

                    for child in gate.children:
                        if child.left.name is None or child.right.name is None:
                            continue
                        working_pairs[child.left.name, child.right.name].add(child)
                        working_pairs[child.right.name, child.left.name].add(child)

        return None

    @staticmethod
    def __names_and_working_pairs(*outputs: BinaryGate) -> tuple[
        dict[str, Bit], defaultdict[tuple[str, str], set[Bit]]]:
        name_to_bit: dict[str, Bit] = {}
        pairs: defaultdict[tuple[str, str], set[Bit]] = defaultdict(lambda: set())

        bit_queue = Queue()
        for output in outputs:
            bit_queue.put(output)

        while not bit_queue.empty():
            bit: Bit = bit_queue.get()
            if bit.name is not None:
                name_to_bit[bit.name] = bit

            if not isinstance(bit, BinaryGate):
                continue
            if bit.left.name is not None and bit.right.name is not None:
                pairs[bit.left.name, bit.right.name].add(bit)
                pairs[bit.right.name, bit.left.name].add(bit)
            bit_queue.put(bit.left)
            bit_queue.put(bit.right)

        return name_to_bit, pairs

    @staticmethod
    def get_all_to_or_gate(*inputs: Bit) -> set[Bit]:
        result = set()
        in_group = set(inputs)
        q = Queue()
        for i in inputs:
            q.put(i)

        while not q.empty():
            test: Bit = q.get()

            child: BinaryGate
            for child in test.children:
                if child in in_group:
                    continue  # Already seen this one

                if child.left not in in_group or child.right not in in_group:
                    continue  # One of the parents isn't in this group, skip it

                result.add(child)
                in_group.add(child)

                if isinstance(child, OrGate):
                    continue  # Don't process these
                q.put(child)

        return result


class Y2024D24(object):
    _debug = False

    def __init__(self, file_name):
        lines = Input(file_name).lines()

        self._incorrect_adder = BadAdder(lines)

    def part1(self):
        result = self._incorrect_adder.result

        print("Part 1:", result)

    def part2(self):
        result = None

        q = Queue()
        q.put(set())

        seen_mismatch = set()

        while not q.empty():
            if self._debug:
                print(q.qsize())
            swappable: frozenset[tuple[str, str]] = q.get()
            try:
                adder = self._incorrect_adder.with_swaps(swappable)
            except AdderLoopException:
                continue  # Whoops, made a loop

            correct_outputs = self._make_full_adder()
            mismatch: tuple[str, str] = adder.find_mismatch(*correct_outputs)
            if mismatch is None:
                result = ','.join(sorted([node for t in swappable for node in t]))
                break

            if mismatch in seen_mismatch:
                continue

            seen_mismatch.add(mismatch)
            seen_mismatch.add((mismatch[1], mismatch[0]))

            if len(swappable) == 4:
                continue  # This didn't work, and we shouldn't try anything new

            mismatched_section = self._find_mismatch_section(adder, mismatch[0], mismatch[1])

            if any([s[0] in mismatched_section and s[1] in mismatched_section for s in swappable]):
                continue  # Same section, this swap did nothing

            if self._debug:
                print(mismatch, mismatched_section)
            for a, b in combinations(mismatched_section, 2):
                union = swappable.union({(a, b)})
                q.put(union)

        print("Part 2:", result)

    def _make_full_adder(self) -> list[BinaryGate]:
        carry = Constant(False)
        correct_outputs: list[BinaryGate] = []
        for i in range(self._incorrect_adder.max_input + 1):
            a = copy(self._incorrect_adder.x(i))
            b = copy(self._incorrect_adder.y(i))

            a_xor_b = a ^ b
            sum_out = a_xor_b ^ carry
            carry = (a & b) | (a_xor_b & carry)
            correct_outputs.append(sum_out)

        correct_outputs.append(carry)
        return correct_outputs

    @staticmethod
    def _find_mismatch_section(adder: BadAdder, a: str, b: str) -> set[str]:
        initial_gate_set = adder.get_all_to_or_gate(
            adder.x(0),
            adder.y(0),
            adder.x(1),
            adder.y(1)
        )

        search_pin = None
        search_data = set()
        carry_gate = None  # Make the "used before instantiation" warning happy.
        for i in range(1, adder.max_input + 1):
            search_data.add(adder.x(i))
            search_data.add(adder.y(i))
            search_data.add(carry_gate)

            if i <= 1:
                gate_set = initial_gate_set
            else:
                gate_set = adder.get_all_to_or_gate(
                    *search_data,
                )
            or_gates = [g for g in gate_set if isinstance(g, OrGate)]
            if len(or_gates) == 0:
                # This swap made it impossible for us to get our bearings. Should be incorrect.
                return set()

            gate_names_set = set(g.name for g in gate_set)

            if a in gate_names_set and b in gate_names_set:
                return gate_names_set

            if a not in gate_names_set and b not in gate_names_set:
                search_data = set()
                carry_gate = or_gates[0]
            elif search_pin is None:
                search_pin = i

            if search_pin is not None:
                for j in range(search_pin, i + 1):
                    search_data.add(adder.x(j))
                    search_data.add(adder.y(j))

        return set()


if __name__ == '__main__':
    code = Y2024D24("2024/24.txt")
    code.part1()
    code.part2()
