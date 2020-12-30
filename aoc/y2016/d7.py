import re
from dataclasses import dataclass
from typing import List

from aoc.util.inputs import Input


@dataclass
class IPV7(object):
    supernets: List[str]
    hypernets: List[str]

    @property
    def supports_tls(self):
        for hypernet in self.hypernets:
            if self._supports_tls(hypernet):
                return False

        for supernet in self.supernets:
            if self._supports_tls(supernet):
                return True

        return False

    @staticmethod
    def _supports_tls(value: str):
        for i in range(len(value) - 3):
            if value[i] == value[i + 3] and \
                    value[i + 1] == value[i + 2] and \
                    value[i] != value[i + 1]:
                return True

        return False

    @property
    def supports_ssl(self):
        for supernet in self.supernets:
            for addr_i in range(len(supernet) - 2):
                if supernet[addr_i] == supernet[addr_i + 2] and supernet[addr_i] != supernet[addr_i + 1]:
                    a = supernet[addr_i]
                    b = supernet[addr_i + 1]
                    check = f"{b}{a}{b}"
                    for hypernet in self.hypernets:
                        if check in hypernet:
                            return True

        return False


class Y2016D7(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.addresses = []

        for line in lines:
            addresses = []
            hypernets = []

            address = ""
            for element in line:
                if element == '[':
                    addresses.append(address)
                    address = ""
                elif element == ']':
                    hypernets.append(address)
                    address = ""
                else:
                    address += element

            if len(address) > 0:
                addresses.append(address)

            self.addresses.append(IPV7(addresses, hypernets))

    def part1(self):
        result = sum(1 for addr in self.addresses if addr.supports_tls)

        print("Part 1:", result)

    def part2(self):
        result = sum(1 for addr in self.addresses if addr.supports_ssl)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2016D7("2016/7.txt")
    code.part1()
    code.part2()
