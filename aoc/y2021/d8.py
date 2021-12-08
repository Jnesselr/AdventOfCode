import itertools
from dataclasses import dataclass
from typing import Dict, List, Set, Optional

from z3 import Solver, Int, Or, And, Distinct

from aoc.util.inputs import Input


@dataclass(frozen=True)
class Segment(object):
    a_wire: str
    b_wire: str
    c_wire: str
    d_wire: str
    e_wire: str
    f_wire: str
    g_wire: str

    def parse(self, display: str):
        display: List[str] = display.split(' ')

        result = ''
        for element in display:
            lit_segments: str = ''.join(sorted([getattr(self, f'{name}_wire') for name in element]))

            if lit_segments == 'abcefg':  # 0
                result += '0'
            elif lit_segments == 'cf':  # 1
                result += '1'
            elif lit_segments == 'acdeg':  # 2
                result += '2'
            elif lit_segments == 'acdfg':  # 3
                result += '3'
            elif lit_segments == 'bcdf':  # 4
                result += '4'
            elif lit_segments == 'abdfg':  # 5
                result += '5'
            elif lit_segments == 'abdefg':  # 6
                result += '6'
            elif lit_segments == 'acf':  # 7
                result += '7'
            elif lit_segments == 'abcdefg':  # 8
                result += '8'
            elif lit_segments == 'abcdfg':  # 9
                result += '9'

        return int(result)


class Y2021D8(object):
    def __init__(self, file_name):
        self._lines = Input(file_name).lines()

    def part1(self):
        result = 0

        for line in self._lines:
            _, tail = line.split('|')
            tail: str = tail.strip()
            for element in tail.split(' '):
                if len(element) in [2, 4, 3, 7]:
                    result += 1

        print("Part 1:", result)

    def part2(self):
        result = 0

        for line in self._lines:
            segment: Segment = self._get_segment(line)

            _, tail = line.split('|')
            tail: str = tail.strip()
            result += segment.parse(tail)

        print("Part 2:", result)

    @staticmethod
    def _get_segment(line: str) -> Segment:
        if '|' in line:
            line: str = line.split('|')[0].strip()

        length_to_set: Dict[int, Set[str]] = {}

        for element in line.split():
            length_to_set.setdefault(len(element), set()).add(element)

        display_one: str = length_to_set[2].copy().pop()
        display_seven: str = length_to_set[3].copy().pop()

        segment_a: str = (set(display_seven) - set(display_one)).pop()

        display_four: str = length_to_set[4].copy().pop()
        extra_for_four: Set[str] = set(display_four) - set(display_one)

        display_zero: Optional[str] = None
        segment_d: Optional[str] = None
        for possibly_display_zero in length_to_set[6]:
            if not set(possibly_display_zero).issuperset(extra_for_four):
                display_zero = possibly_display_zero

                for segment in extra_for_four:
                    if segment not in display_zero:
                        segment_d = segment

                break

        if display_zero is None or segment_d is None:
            raise Exception("Display zero or segment d are None")

        six_or_nine = length_to_set[6].copy()
        six_or_nine.remove(display_zero)

        display_six: Optional[str] = None
        display_nine: Optional[str] = None
        for display in six_or_nine:
            if set(display_one).issubset(display):
                display_nine = display
            else:
                display_six = display

        if display_six is None or display_nine is None:
            raise Exception("Display six or nine are None")

        segment_e = (set('abcdefg') - set(display_nine)).pop()
        segment_c = (set('abcdefg') - set(display_six)).pop()
        segment_f = (set(display_one) - set(segment_c)).pop()
        segment_b = (set(display_four) - set(display_one) - set(segment_d)).pop()
        segment_g = (set('abcdefg') - set(display_four) - set(display_seven) - set(segment_e)).pop()

        wires = {}
        wires[segment_a] = 'a'
        wires[segment_b] = 'b'
        wires[segment_c] = 'c'
        wires[segment_d] = 'd'
        wires[segment_e] = 'e'
        wires[segment_f] = 'f'
        wires[segment_g] = 'g'

        return Segment(
            a_wire=wires['a'],
            b_wire=wires['b'],
            c_wire=wires['c'],
            d_wire=wires['d'],
            e_wire=wires['e'],
            f_wire=wires['f'],
            g_wire=wires['g']
        )


if __name__ == '__main__':
    code = Y2021D8("2021/8.txt")
    code.part1()
    code.part2()
