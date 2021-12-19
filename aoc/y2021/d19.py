import enum
import itertools
import re
from collections import Counter
from dataclasses import dataclass
from queue import Queue
from typing import Dict, List, Set

from aoc.util.inputs import Input


class Reorientation(enum.Enum):
    POS_X_TO_POS_X = enum.auto()
    POS_X_TO_NEG_X = enum.auto()
    POS_X_TO_POS_Y = enum.auto()
    POS_X_TO_NEG_Y = enum.auto()
    POS_X_TO_POS_Z = enum.auto()
    POS_X_TO_NEG_Z = enum.auto()
    POS_Y_TO_POS_X = enum.auto()
    POS_Y_TO_NEG_X = enum.auto()
    POS_Y_TO_POS_Y = enum.auto()
    POS_Y_TO_NEG_Y = enum.auto()
    POS_Y_TO_POS_Z = enum.auto()
    POS_Y_TO_NEG_Z = enum.auto()
    POS_Z_TO_POS_X = enum.auto()
    POS_Z_TO_NEG_X = enum.auto()
    POS_Z_TO_POS_Y = enum.auto()
    POS_Z_TO_NEG_Y = enum.auto()
    POS_Z_TO_POS_Z = enum.auto()
    POS_Z_TO_NEG_Z = enum.auto()


@dataclass(frozen=True)
class Beacon(object):
    x: int
    y: int
    z: int


@dataclass(frozen=True)
class Scanner(object):
    num: int
    x: int
    y: int
    z: int

    def manhattan(self, other: 'Scanner'):
        return abs(other.x - self.x) + abs(other.y - self.y) + abs(other.z - self.z)


class Y2021D19(object):
    def __init__(self, file_name):
        groups = Input(file_name).grouped()
        self._beacons: Dict[int, List[Beacon]] = {}
        self._scanners: Dict[int, Scanner] = {0: Scanner(0, 0, 0, 0)}

        scanner_regex = re.compile(r'--- scanner (\d+) ---')
        for group in groups:
            scanner_number = int(scanner_regex.match(group[0]).group(1))
            beacons: List[Beacon] = []
            for line in group[1:]:
                x, y, z = line.split(',')
                beacons.append(Beacon(
                    x=int(x),
                    y=int(y),
                    z=int(z)
                ))

            self._beacons[scanner_number] = beacons

        queue = Queue()
        queue.put(self._scanners[0])

        while not queue.empty():
            scanner: Scanner = queue.get()
            my_beacons = self._beacons[scanner.num]

            for scan_num, beacons in self._beacons.items():
                if scan_num in self._scanners:
                    continue

                reorientations = dict(self._maybe_get_reorientations(my_beacons, beacons))

                if len(reorientations) == 3:
                    # print(f"Going to reorient {scan_num} from {scanner.num}")
                    new_scanner, new_beacons = self._reorient(scan_num, reorientations)
                    # print(new_scanner)
                    self._scanners[scan_num] = new_scanner
                    self._beacons[scan_num] = new_beacons
                    queue.put(new_scanner)

    def part1(self):
        all_beacons: Set = set()
        for beacons in self._beacons.values():
            for beacon in beacons:
                all_beacons.add(beacon)

        result = len(all_beacons)

        print("Part 1:", result)

    def part2(self):
        result = 0

        for left, right in itertools.product(self._scanners.values(), repeat=2):
            if left is right:
                continue

            result = max(result, left.manhattan(right))

        print("Part 2:", result)

    def _reorient(self,
                  new_scanner_number: int,
                  reorientations: Dict[Reorientation, int]):
        new_x = None
        new_y = None
        new_z = None
        new_x_beacons = None
        new_y_beacons = None
        new_z_beacons = None
        beacons = self._beacons[new_scanner_number]
        for reorientation, value in reorientations.items():
            if reorientation == Reorientation.POS_X_TO_POS_X:  # ?
                new_x = -value
                new_x_beacons = [b.x + new_x for b in beacons]
            elif reorientation == Reorientation.POS_X_TO_NEG_X:  # ?/!
                new_x = -value
                new_x_beacons = [-b.x + new_x for b in beacons]
            elif reorientation == Reorientation.POS_X_TO_POS_Y:  # ?
                new_y = -value
                new_y_beacons = [b.x + new_y for b in beacons]
            elif reorientation == Reorientation.POS_X_TO_NEG_Y:  # ?
                new_y = -value
                new_y_beacons = [-b.x + new_y for b in beacons]
            elif reorientation == Reorientation.POS_X_TO_POS_Z:  # ?
                new_z = -value
                new_z_beacons = [b.x + new_z for b in beacons]
            elif reorientation == Reorientation.POS_X_TO_NEG_Z:  # ?
                new_z = -value
                new_z_beacons = [-b.x + new_z for b in beacons]
            elif reorientation == Reorientation.POS_Y_TO_POS_X:  # ?
                new_x = -value
                new_x_beacons = [b.y + new_x for b in beacons]
            elif reorientation == Reorientation.POS_Y_TO_NEG_X:  # ?
                new_x = -value
                new_x_beacons = [-b.y + new_x for b in beacons]
            elif reorientation == Reorientation.POS_Y_TO_POS_Y:  # ?/!
                new_y = -value
                new_y_beacons = [b.y + new_y for b in beacons]
            elif reorientation == Reorientation.POS_Y_TO_NEG_Y:  # ?
                new_y = -value
                new_y_beacons = [-b.y + new_y for b in beacons]
            elif reorientation == Reorientation.POS_Y_TO_POS_Z:  # ?
                new_z = -value
                new_z_beacons = [b.y + new_z for b in beacons]
            elif reorientation == Reorientation.POS_Y_TO_NEG_Z:  # ?
                new_z = -value
                new_z_beacons = [-b.y + new_z for b in beacons]
            elif reorientation == Reorientation.POS_Z_TO_POS_X:  # ?
                new_x = -value
                new_x_beacons = [b.z + new_x for b in beacons]
            elif reorientation == Reorientation.POS_Z_TO_NEG_X:  # ?
                new_x = -value
                new_x_beacons = [-b.z + new_x for b in beacons]
            elif reorientation == Reorientation.POS_Z_TO_POS_Y:  # ?
                new_y = -value
                new_y_beacons = [b.z + new_y for b in beacons]
            elif reorientation == Reorientation.POS_Z_TO_NEG_Y:  # ?
                new_y = -value
                new_y_beacons = [-b.z + new_y for b in beacons]
            elif reorientation == Reorientation.POS_Z_TO_POS_Z:  # ?
                new_z = -value
                new_z_beacons = [b.z + new_z for b in beacons]
            elif reorientation == Reorientation.POS_Z_TO_NEG_Z:  # ?/
                new_z = -value
                new_z_beacons = [-b.z + new_z for b in beacons]

        scanner = Scanner(new_scanner_number, new_x, new_y, new_z)
        new_beacons = [Beacon(x, y, z) for x, y, z in zip(new_x_beacons, new_y_beacons, new_z_beacons)]
        return scanner, new_beacons

    @staticmethod
    def _maybe_get_reorientations(left_beacons: List[Beacon],
                                  right_beacons: List[Beacon]):
        # pdx_mdx means the positive x of the right beacon is the negative x of the left
        pdx_pdx = Counter([rb.x - lb.x for lb, rb in itertools.product(left_beacons, right_beacons)]).most_common()[0]
        pdx_mdx = Counter([-rb.x - lb.x for lb, rb in itertools.product(left_beacons, right_beacons)]).most_common()[0]
        pdx_pdy = Counter([rb.x - lb.y for lb, rb in itertools.product(left_beacons, right_beacons)]).most_common()[0]
        pdx_mdy = Counter([-rb.x - lb.y for lb, rb in itertools.product(left_beacons, right_beacons)]).most_common()[0]
        pdx_pdz = Counter([rb.x - lb.z for lb, rb in itertools.product(left_beacons, right_beacons)]).most_common()[0]
        pdx_mdz = Counter([-rb.x - lb.z for lb, rb in itertools.product(left_beacons, right_beacons)]).most_common()[0]

        pdy_pdx = Counter([rb.y - lb.x for lb, rb in itertools.product(left_beacons, right_beacons)]).most_common()[0]
        pdy_mdx = Counter([-rb.y - lb.x for lb, rb in itertools.product(left_beacons, right_beacons)]).most_common()[0]
        pdy_pdy = Counter([rb.y - lb.y for lb, rb in itertools.product(left_beacons, right_beacons)]).most_common()[0]
        pdy_mdy = Counter([-rb.y - lb.y for lb, rb in itertools.product(left_beacons, right_beacons)]).most_common()[0]
        pdy_pdz = Counter([rb.y - lb.z for lb, rb in itertools.product(left_beacons, right_beacons)]).most_common()[0]
        pdy_mdz = Counter([-rb.y - lb.z for lb, rb in itertools.product(left_beacons, right_beacons)]).most_common()[0]

        pdz_pdx = Counter([rb.z - lb.x for lb, rb in itertools.product(left_beacons, right_beacons)]).most_common()[0]
        pdz_mdx = Counter([-rb.z - lb.x for lb, rb in itertools.product(left_beacons, right_beacons)]).most_common()[0]
        pdz_pdy = Counter([rb.z - lb.y for lb, rb in itertools.product(left_beacons, right_beacons)]).most_common()[0]
        pdz_mdy = Counter([-rb.z - lb.y for lb, rb in itertools.product(left_beacons, right_beacons)]).most_common()[0]
        pdz_pdz = Counter([rb.z - lb.z for lb, rb in itertools.product(left_beacons, right_beacons)]).most_common()[0]
        pdz_mdz = Counter([-rb.z - lb.z for lb, rb in itertools.product(left_beacons, right_beacons)]).most_common()[0]

        if pdx_pdx[1] >= 12:
            yield Reorientation.POS_X_TO_POS_X, pdx_pdx[0]
        elif pdx_mdx[1] >= 12:
            yield Reorientation.POS_X_TO_NEG_X, pdx_mdx[0]
        elif pdx_pdy[1] >= 12:
            yield Reorientation.POS_X_TO_POS_Y, pdx_pdy[0]
        elif pdx_mdy[1] >= 12:
            yield Reorientation.POS_X_TO_NEG_Y, pdx_mdy[0]
        elif pdx_pdz[1] >= 12:
            yield Reorientation.POS_X_TO_POS_Z, pdx_pdz[0]
        elif pdx_mdz[1] >= 12:
            yield Reorientation.POS_X_TO_NEG_Z, pdx_mdz[0]

        if pdy_pdx[1] >= 12:
            yield Reorientation.POS_Y_TO_POS_X, pdy_pdx[0]
        elif pdy_mdx[1] >= 12:
            yield Reorientation.POS_Y_TO_NEG_X, pdy_mdx[0]
        elif pdy_pdy[1] >= 12:
            yield Reorientation.POS_Y_TO_POS_Y, pdy_pdy[0]
        elif pdy_mdy[1] >= 12:
            yield Reorientation.POS_Y_TO_NEG_Y, pdy_mdy[0]
        elif pdy_pdz[1] >= 12:
            yield Reorientation.POS_Y_TO_POS_Z, pdy_pdz[0]
        elif pdy_mdz[1] >= 12:
            yield Reorientation.POS_Y_TO_NEG_Z, pdy_mdz[0]

        if pdz_pdx[1] >= 12:
            yield Reorientation.POS_Z_TO_POS_X, pdz_pdx[0]
        elif pdz_mdx[1] >= 12:
            yield Reorientation.POS_Z_TO_NEG_X, pdz_mdx[0]
        elif pdz_pdy[1] >= 12:
            yield Reorientation.POS_Z_TO_POS_Y, pdz_pdy[0]
        elif pdz_mdy[1] >= 12:
            yield Reorientation.POS_Z_TO_NEG_Y, pdz_mdy[0]
        elif pdz_pdz[1] >= 12:
            yield Reorientation.POS_Z_TO_POS_Z, pdz_pdz[0]
        elif pdz_mdz[1] >= 12:
            yield Reorientation.POS_Z_TO_NEG_Z, pdz_mdz[0]


if __name__ == '__main__':
    code = Y2021D19("2021/19.txt")
    code.part1()
    code.part2()
