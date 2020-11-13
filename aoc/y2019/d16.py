from aoc.util.inputs import Input


class Y2019D16(object):
    def __init__(self, file_name):
        line = Input(file_name).line()
        self.input = [int(x) for x in line]

    def _get_pattern(self, index):
        zeros = [0] * (index + 1)
        ones = [1] * (index + 1)
        negatives = [-1] * (index + 1)

        base_pattern = zeros + ones + zeros + negatives
        multiplier = (len(self.input) // len(base_pattern)) + 1

        pattern = base_pattern * multiplier
        return pattern[1:]

    def part1(self):
        phase = self.input.copy()
        next_phase = []
        for _ in range(100):
            for index in range(len(self.input)):
                pattern = self._get_pattern(index)
                next_phase.append(abs(sum([x * y for x, y in zip(phase, pattern)])) % 10)
            phase = next_phase
            next_phase = []

        result = "".join(str(x) for x in phase[:8])

        print("Part 1:", result)

    def part2(self):
        phase = self.input * 10000
        offset = int("".join(str(x) for x in phase[:7]))

        # This ONLY works if this condition is met. Explained in a comment at the bottom of this file.
        assert offset * 2 > len(phase)

        phase = phase[offset:]
        phase_length = len(phase)

        for _ in range(100):
            for index in range(phase_length - 2, -1, -1):
                phase[index] = (phase[index] + phase[index + 1]) % 10

        result = "".join(str(x) for x in phase[:8])

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2019D16("2019/16.txt")
    code.part1()
    code.part2()

"""
There's a shortcut for part 2 that we have to use. We rely in a few observations:
1. The last phase index always has a 1 for that index and 0s for everything else. In other words, the last digit never
  actually changes.
2. For every index previously, up to a point, it's 1s from that index until the end.
3. The point that stops being the case is at index k where 2*k <= N (N being the length of the phase). If you think
  about it, at index k, we have (k-1) 0s and then k ones. If we want 1s until the end of the phase, we can't have
  (k-1) + k end short of the end of the phase. This means that (k-1) + k < N is a bad thing. We just add 1 to the left
  side, simplifying it to 2 * k and change the < to <= being bad. That's why the 2 * k > N assertion is there.
3. Since it's all modulo 10, adding the elements from index x to index y is the same as a adding index x + (x+1 to y).
  We start with y and go backwards from y to x.
"""