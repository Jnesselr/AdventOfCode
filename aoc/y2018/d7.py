import re
from dataclasses import dataclass
from typing import Set, Optional, Dict

from aoc.util.inputs import Input
from aoc.util.queue import PriorityQueue
from aoc.util.tasks import Tasking


@dataclass(frozen=True)
class WithTime(object):
    value: Optional[str]
    time: int


class Y2018D7(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()

        self.tasking: Tasking[str] = Tasking[str]()

        for line in lines:
            matched = re.match(r"Step (\w) must be finished before step (\w) can begin.", line)
            self.tasking.requires(matched.group(2), matched.group(1))

    def part1(self):
        tasking = self.tasking.copy()
        result = ""

        while tasking:
            min_element = min(tasking.available_tasks)
            result += min_element
            tasking.done(min_element)

        print("Part 1:", result)

    def part2(self):
        tasking = self.tasking.copy()
        queue: PriorityQueue[WithTime] = PriorityQueue[WithTime]()
        for _ in range(5):
            queue.push(WithTime(None, 0), 0)

        current_tasks: Dict[str, int] = {}

        biggest_time = 0

        while tasking:
            completed_task: WithTime = queue.pop()

            if completed_task.value is not None:
                tasking.done(completed_task.value)
                del current_tasks[completed_task.value]

            available_tasks = [task for task in tasking.available_tasks if task not in current_tasks]

            if len(available_tasks) == 0:
                if len(current_tasks) > 0:
                    # This worker has no task at least until the next task finishes
                    check_time = min(current_tasks.values())
                    queue.push(WithTime(None, check_time), check_time)
                continue

            next_task = min(available_tasks)
            next_time = completed_task.time + ord(next_task) - 4
            current_tasks[next_task] = next_time
            biggest_time = max(biggest_time, next_time)
            queue.push(WithTime(next_task, next_time), next_time)

        result = biggest_time

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2018D7("2018/7.txt")
    code.part1()
    code.part2()
