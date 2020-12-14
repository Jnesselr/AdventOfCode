import re

from aoc.util.inputs import Input


class Y2020D14(object):
    def __init__(self, file_name):
        self.lines = Input(file_name).lines()

    def part1(self):
        memory = {}

        zero_mask = 0
        one_mask = 0
        for line in self.lines:
            if (matched := re.match(r'mask = (.*)', line)) is not None:
                mask = matched.group(1)
                zero_mask = int(mask.replace('X', '1'), 2)
                one_mask = int(mask.replace('X', '0'), 2)
            elif (matched := re.match(r'mem\[(\d+)] = (\d+)', line)) is not None:
                address = int(matched.group(1))
                value = int(matched.group(2))
                value &= zero_mask
                value |= one_mask
                memory[address] = value

        result = sum(memory.values())

        print("Part 1:", result)

    def part2(self):
        memory = {}

        mask = None
        zero_mask = 0
        one_mask = 0
        for line in self.lines:
            if (matched := re.match(r'mask = (.*)', line)) is not None:
                mask = matched.group(1)
                zero_mask = int(mask.replace('0', '1').replace('X', '0'), 2)
                one_mask = int(mask.replace('X', '0'), 2)
            elif (matched := re.match(r'mem\[(\d+)] = (\d+)', line)) is not None:
                address = int(matched.group(1))
                address &= zero_mask
                address |= one_mask
                value = int(matched.group(2))

                addresses = {address}
                for index, bit_value in enumerate(reversed(mask)):
                    if bit_value != 'X':
                        continue

                    bit_mask = 1 << index
                    inverted_bit_mask = (2 ** 36 - 1) - bit_mask
                    for address in addresses.copy():
                        addresses.add(address & inverted_bit_mask)
                        addresses.add(address | bit_mask)

                for address in addresses:
                    memory[address] = value

        result = sum(memory.values())

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2020D14("2020/14.txt")
    code.part1()
    code.part2()
