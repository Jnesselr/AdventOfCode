from dataclasses import dataclass
from typing import Generic, TypeVar, Dict, Set

T = TypeVar('T')


class Tasking(Generic[T]):
    def __init__(self):
        self._dependents: Dict[T, Set[T]] = {}
        self._requirements: Dict[T, Set[T]] = {}

    def __bool__(self):
        return len(self._requirements) > 0

    def copy(self):
        result: Tasking[T] = Tasking[T]()

        for task, required_set in self._requirements.items():
            for required in required_set:
                result.requires(task, required)

        return result

    def requires(self, task: T, required: T):
        self._dependents.setdefault(task, set())
        self._dependents.setdefault(required, set()).add(task)

        self._requirements.setdefault(required, set())
        self._requirements.setdefault(task, set()).add(required)

    def done(self, task: T):
        requirements = self._requirements[task]

        if len(requirements) > 0:
            raise ValueError("Can't complete that task, it has requirements!")

        for dependent in self._dependents[task]:
            self._requirements[dependent].remove(task)

        del self._dependents[task]
        del self._requirements[task]

    @property
    def available_tasks(self):
        return set(key for key, value in self._requirements.items() if len(value) == 0)
