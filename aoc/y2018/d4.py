import re
from dataclasses import dataclass

from aoc.util.inputs import Input


@dataclass(frozen=True)
class GuardSleeping(object):
    id: int
    start_time: int
    end_time: int


class Y2018D4(object):
    def __init__(self, file_name):
        lines = sorted(Input(file_name).lines())
        current_guard = None
        sleep_start = None

        self.guards = []

        for line in lines:
            begins_shift = re.match(r"\[.*] Guard #(\d+) begins shift", line)
            falls_asleep = re.match(r"\[.* 00:(\d+)] falls asleep", line)
            wakes_up = re.match(r"\[.* 00:(\d+)] wakes up", line)

            if begins_shift is not None:
                current_guard = int(begins_shift.group(1))
            elif falls_asleep is not None:
                sleep_start = int(falls_asleep.group(1))
            elif wakes_up is not None:
                end_time = int(wakes_up.group(1)) - 1
                self.guards.append(GuardSleeping(current_guard, sleep_start, end_time))
            else:
                raise ValueError("All are None!")

    def part1(self):
        guards_to_times = {}

        for guard in self.guards:
            if guard.id not in guards_to_times:
                guards_to_times[guard.id] = 0
            guards_to_times[guard.id] += (guard.end_time - guard.start_time + 1)

        worst_guard, _ = max(guards_to_times.items(), key=lambda x: x[1])
        worst_guard_times = {}

        for guard in self.guards:
            if guard.id != worst_guard:
                continue

            for time in range(guard.start_time, guard.end_time + 1):
                if time not in worst_guard_times:
                    worst_guard_times[time] = 0
                worst_guard_times[time] += 1

        worst_time, _ = max(worst_guard_times.items(), key=lambda x: x[1])

        result = worst_guard * worst_time

        print("Part 1:", result)

    def part2(self):
        guards_to_times = {}
        # {id -> {time -> count}}

        for guard in self.guards:
            if guard.id not in guards_to_times:
                guards_to_times[guard.id] = {}

            for time in range(guard.start_time, guard.end_time + 1):
                if time not in guards_to_times[guard.id]:
                    guards_to_times[guard.id][time] = 0
                guards_to_times[guard.id][time] += 1

        # Find the worst guard by getting the largest time for that guard then the guard with the largest time overall
        # Then once again find the largest time for our worst guard.
        worst_guard, _ = max(guards_to_times.items(), key=lambda x: max(x[1].items(), key=lambda y: y[1])[1])
        worst_time, _ = max(guards_to_times[worst_guard].items(), key=lambda x: x[1])
        result = worst_guard * worst_time

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2018D4("2018/4.txt")
    code.part1()
    code.part2()
