from aoc.util.inputs import Input


class Y2015D19(object):
    def __init__(self, file_name):
        transformations, medicine = Input(file_name).grouped()

        self.medicine = medicine.pop()
        self.forward = {}
        self.backward = {}

        for transform in transformations:
            _in, _out = transform.split(' => ')
            self.forward.setdefault(_in, set()).add(_out)
            self.backward[_out] = _in

    def part1(self):
        distinct_molecules = set()

        index = 0
        while index < len(self.medicine):
            element = self.medicine[index]
            if index + 1 < len(self.medicine) and self.medicine[index + 1].islower():
                element = self.medicine[index:index + 2]

            if element in self.forward:
                for out in self.forward[element]:
                    modified = self.medicine[:index] + out + self.medicine[index + len(element):]
                    distinct_molecules.add(modified)

            index += len(element)

        result = len(distinct_molecules)

        print("Part 1:", result)

    def part2(self):
        molecule: str = self.medicine
        steps = 0

        while len(molecule) > 1:
            possible_replacements = set()
            for m in self.backward.keys():
                if m in molecule:
                    possible_replacements.add(m)

            replacements = sorted(list(possible_replacements), key=lambda x: -molecule.rindex(x))
            next_replacement = replacements[0]

            replacement_index = molecule.rindex(next_replacement)
            replacement = self.backward[next_replacement]
            molecule = molecule[:replacement_index] + replacement + molecule[replacement_index+len(next_replacement):]
            steps += 1

        result = steps

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2015D19("2015/19.txt")
    code.part1()
    code.part2()
