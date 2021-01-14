import itertools

from aoc.util.inputs import Input


class Y2015D17(object):
    def __init__(self, file_name):
        containers = Input(file_name).ints()

        self.num_combinations = 0
        self.num_with_min_containers = 0
        min_containers = len(containers)

        for count in range(len(containers)):
            for combination in itertools.combinations(containers, r=count):
                if sum(combination) == 150:
                    self.num_combinations += 1

                    if count < min_containers:
                        self.num_with_min_containers = 0
                        min_containers = count
                    if count == min_containers:
                        self.num_with_min_containers += 1

    def part1(self):
        result = self.num_combinations

        print("Part 1:", result)

    def part2(self):
        result = self.num_with_min_containers

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2015D17("2015/17.txt")
    code.part1()
    code.part2()
