from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property

from aoc.util.inputs import Input


@dataclass
class Initialization:
    value: str

    @property
    def focal_length(self) -> int:
        if '-' in self.value:
            return 0

        _, focal_length = self.value.split('=')
        return int(focal_length)

    @cached_property
    def lens(self):
        if '-' in self.value:
            return self.value[:-1]

        lens, _ = self.value.split('=')
        return lens

    @property
    def value_hash(self) -> int:
        result = 0

        for ch in self.value:
            result += ord(ch)
            result *= 17
            result %= 256

        return result

    def __hash__(self) -> int:
        result = 0

        for ch in self.value:
            if ch in '-=':
                return result

            result += ord(ch)
            result *= 17
            result %= 256

        return result


class Y2023D15(object):
    def __init__(self, file_name):
        self._initialization_sequence = [Initialization(v.strip()) for v in Input(file_name).line().split(',')]

    def part1(self):
        result = sum(i.value_hash for i in self._initialization_sequence)

        print("Part 1:", result)

    def part2(self):
        result = 0

        boxes: defaultdict[int, dict[int, Initialization]] = defaultdict(lambda: {})

        for init in self._initialization_sequence:
            box = boxes[hash(init)]

            slot_array = [s for s, i in box.items() if i.lens == init.lens]

            if '-' in init.value:  # Removing a lens
                if len(slot_array) == 0:
                    continue  # Nothing to do here

                del box[slot_array[0]]  # Remove the lens we matched with

                # Move everything down one
                target_slot = 1
                while True:
                    min_array = [s for s in box.keys() if s >= target_slot]
                    if len(min_array) == 0:
                        break  # We've moved everything down

                    from_value = min(min_array)
                    if from_value != target_slot:
                        box[target_slot] = box[from_value]
                        del box[from_value]
                    target_slot += 1

            elif len(slot_array) == 0:  # = with lens not in the box
                max_array = [s for s in box.keys()]
                if len(max_array) == 0:  # Empty box
                    box[1] = init
                else:
                    box[max(max_array) + 1] = init

            else:  # = with lens in box
                box[slot_array[0]] = init

        for box, lenses in boxes.items():
            for slot, init in lenses.items():
                result += (box + 1) * slot * init.focal_length
        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2023D15("2023/15.txt")
    code.part1()
    code.part2()
