import re
from dataclasses import dataclass, field
from queue import Queue
from typing import Optional

from aoc.util.inputs import Input


@dataclass(frozen=True)
class Part:
    x: int
    m: int
    a: int
    s: int

    def get_value(self, name: str):
        if name == 'x':
            return self.x
        elif name == 'm':
            return self.m
        elif name == 'a':
            return self.a
        elif name == 's':
            return self.s


@dataclass(frozen=True)
class WorkflowStep:
    variable: str
    operation: str
    value: int
    goto: str


@dataclass(frozen=True)
class PartRange:
    workflow_name: str = field(default='in')
    min_x: int = field(default=1)
    max_x: int = field(default=4000)
    min_m: int = field(default=1)
    max_m: int = field(default=4000)
    min_a: int = field(default=1)
    max_a: int = field(default=4000)
    min_s: int = field(default=1)
    max_s: int = field(default=4000)

    @property
    def count(self):
        return (self.max_x - self.min_x + 1) * \
            (self.max_m - self.min_m + 1) * \
            (self.max_a - self.min_a + 1) * \
            (self.max_s - self.min_s + 1)

    def with_new_name(self, new_name: str) -> 'PartRange':
        return PartRange(
            workflow_name=new_name,
            min_x=self.min_x, max_x=self.max_x, min_m=self.min_m, max_m=self.max_m,
            min_a=self.min_a, max_a=self.max_a, min_s=self.min_s, max_s=self.max_s,
        )

    def split_x(self, x: int) -> tuple[Optional['PartRange'], Optional['PartRange']]:
        if x < self.min_x:
            return None, self
        elif x > self.max_x:
            return self, None

        lower = PartRange(
            workflow_name=self.workflow_name,
            min_x=self.min_x, min_m=self.min_m, max_m=self.max_m,
            min_a=self.min_a, max_a=self.max_a, min_s=self.min_s, max_s=self.max_s,

            max_x=x
        )
        upper = PartRange(
            workflow_name=self.workflow_name,
            max_x=self.max_x, min_m=self.min_m, max_m=self.max_m,
            min_a=self.min_a, max_a=self.max_a, min_s=self.min_s, max_s=self.max_s,
            min_x=x + 1
        )
        return lower, upper

    def split_m(self, m: int) -> tuple[Optional['PartRange'], Optional['PartRange']]:
        if m < self.min_m:
            return None, self
        elif m > self.max_m:
            return self, None

        lower = PartRange(
            workflow_name=self.workflow_name,
            min_x=self.min_x, max_x=self.max_x, min_m=self.min_m,
            min_a=self.min_a, max_a=self.max_a, min_s=self.min_s, max_s=self.max_s,
            max_m=m
        )
        upper = PartRange(
            workflow_name=self.workflow_name,
            min_x=self.min_x, max_x=self.max_x, max_m=self.max_m,
            min_a=self.min_a, max_a=self.max_a, min_s=self.min_s, max_s=self.max_s,
            min_m=m + 1
        )
        return lower, upper

    def split_a(self, a: int) -> tuple[Optional['PartRange'], Optional['PartRange']]:
        if a < self.min_a:
            return None, self
        elif a > self.max_a:
            return self, None

        lower = PartRange(
            workflow_name=self.workflow_name,
            min_x=self.min_x, max_x=self.max_x, min_m=self.min_m, max_m=self.max_m,
            min_a=self.min_a, min_s=self.min_s, max_s=self.max_s,
            max_a=a
        )
        upper = PartRange(
            workflow_name=self.workflow_name,
            min_x=self.min_x, max_x=self.max_x, min_m=self.min_m, max_m=self.max_m,
            max_a=self.max_a, min_s=self.min_s, max_s=self.max_s,
            min_a=a + 1
        )
        return lower, upper

    def split_s(self, s: int) -> tuple[Optional['PartRange'], Optional['PartRange']]:
        if s < self.min_s:
            return None, self
        elif s > self.max_s:
            return self, None

        lower = PartRange(
            workflow_name=self.workflow_name,
            min_x=self.min_x, max_x=self.max_x, min_m=self.min_m, max_m=self.max_m,
            min_a=self.min_a, max_a=self.max_a, min_s=self.min_s,
            max_s=s
        )
        upper = PartRange(
            workflow_name=self.workflow_name,
            min_x=self.min_x, max_x=self.max_x, min_m=self.min_m, max_m=self.max_m,
            min_a=self.min_a, max_a=self.max_a, max_s=self.max_s,
            min_s=s + 1
        )
        return lower, upper

    def split(self, step: WorkflowStep) -> tuple[Optional['PartRange'], Optional['PartRange']]:
        if step.variable == 'x' and step.operation == '<':
            passes_step, fails_step = self.split_x(step.value - 1)
        elif step.variable == 'x' and step.operation == '>':
            fails_step, passes_step = self.split_x(step.value)
        elif step.variable == 'm' and step.operation == '<':
            passes_step, fails_step = self.split_m(step.value - 1)
        elif step.variable == 'm' and step.operation == '>':
            fails_step, passes_step = self.split_m(step.value)
        elif step.variable == 'a' and step.operation == '<':
            passes_step, fails_step = self.split_a(step.value - 1)
        elif step.variable == 'a' and step.operation == '>':
            fails_step, passes_step = self.split_a(step.value)
        elif step.variable == 's' and step.operation == '<':
            passes_step, fails_step = self.split_s(step.value - 1)
        elif step.variable == 's' and step.operation == '>':
            fails_step, passes_step = self.split_s(step.value)
        else:
            raise ValueError("Unknown step variable")

        if passes_step is None:
            return None, fails_step

        return passes_step.with_new_name(step.goto), fails_step


@dataclass
class Workflow:
    name: str
    default: str
    steps: list[WorkflowStep] = field(default_factory=lambda: [])

    def run(self, part: Part):
        for step in self.steps:
            part_value = part.get_value(step.variable)
            if step.operation == '<' and part_value < step.value:
                return step.goto
            if step.operation == '>' and part_value > step.value:
                return step.goto

        return self.default

    def split(self, pr: PartRange):
        if pr.workflow_name != self.name:
            raise ValueError("Part range was called on different workflow")

        # Each step, we'll either split off all of our range or carry it over to the next step
        for step in self.steps:
            passes_step, next_pr = pr.split(step)

            if passes_step is not None:
                yield passes_step

            if next_pr is None:
                return  # Nothing more to do
            pr = next_pr

        yield pr.with_new_name(self.default)


class Y2023D19(object):
    def __init__(self, file_name):
        workflows, parts = Input(file_name).grouped()

        workflow_re = re.compile(r'(\w+){(.*),(\w+)}')
        workflow_step_re = re.compile(r'(\w+)([<>])(\d+):(\w+)')

        self.workflows: dict[str, Workflow] = {}

        for line in workflows:
            match = workflow_re.match(line)

            workflow = Workflow(
                name=match.group(1),
                default=match.group(3)
            )
            for step in match.group(2).split(','):
                match_step = workflow_step_re.match(step)
                step = WorkflowStep(
                    variable=match_step.group(1),
                    operation=match_step.group(2),
                    value=int(match_step.group(3)),
                    goto=match_step.group(4)
                )
                workflow.steps.append(step)

            self.workflows[workflow.name] = workflow

        part_re = re.compile(r'{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}')

        self.parts: list[Part] = []
        for line in parts:
            match = part_re.match(line)
            self.parts.append(Part(
                x=int(match.group(1)),
                m=int(match.group(2)),
                a=int(match.group(3)),
                s=int(match.group(4))
            ))

    def part1(self):
        result = 0

        for part in self.parts:
            workflow_name = 'in'
            while workflow_name not in 'AR':
                workflow = self.workflows[workflow_name]
                workflow_name = workflow.run(part)

            if workflow_name == 'A':
                result += part.x + part.m + part.a + part.s

        print("Part 1:", result)

    def part2(self):
        result = 0

        q = Queue()
        q.put(PartRange())
        while not q.empty():
            pr: PartRange = q.get()
            workflow: Workflow = self.workflows.get(pr.workflow_name)
            for new_pr in workflow.split(pr):
                if new_pr.workflow_name == 'A':
                    result += new_pr.count
                    continue
                elif new_pr.workflow_name == 'R':
                    continue
                q.put(new_pr)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2023D19("2023/19.txt")
    code.part1()
    code.part2()
