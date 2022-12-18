import enum
from typing import TypeVar, Generic, Dict, Optional

T = TypeVar('T')


class CycleStatus(enum.Enum):
    UNKNOWN = enum.auto()
    TESTING = enum.auto()
    FOUND = enum.auto()


class CycleFinder(Generic[T]):
    def __init__(self, wait_at_least=None, needs_repeated=1):
        self._cache: Dict[int, T] = {}
        self._last_seen_index: Dict[T, int] = {}
        self._cycle_status: CycleStatus = CycleStatus.UNKNOWN
        self._cycle_start: Optional[int] = None
        self._cycle_end: Optional[int] = None
        self._testing_index: Optional[int] = None

        self._wait_at_least: Optional[int] = wait_at_least
        self._repeat_count = 0
        self._needs_repeated: int = needs_repeated

    @property
    def cycle_found(self) -> bool:
        return self._cycle_status == CycleStatus.FOUND

    @property
    def cycle_start(self) -> Optional[int]:
        if not self.cycle_found:
            return None
        return self._cycle_start

    @property
    def cycle_size(self) -> Optional[int]:
        if not self.cycle_found:
            return None
        return self._cycle_end - self._cycle_start + 1

    def __setitem__(self, index: int, value: T):
        if self._cycle_status == CycleStatus.FOUND:
            return

        last_seen_index = self._last_seen_index[value] if value in self._last_seen_index else None

        self._last_seen_index[value] = index
        self._cache[index] = value

        if last_seen_index is None:
            self._reset()  # Can't be in a cycle if this is a new number
            return

        if self._wait_at_least is not None and index < self._wait_at_least:
            return

        if self._cycle_status == CycleStatus.UNKNOWN:
            self._repeat_count = 0
            self._cycle_start = last_seen_index
            self._testing_index = last_seen_index
            self._cycle_end = index - 1
            self._cycle_status = CycleStatus.TESTING
        elif self._cycle_status == CycleStatus.TESTING:
            self._testing_index += 1
            if self._cache[self._testing_index] != value:  # We've broken the cycle
                self._reset()
                return

            if self._cycle_end == self._testing_index:
                self._repeat_count += 1
                if self._repeat_count == self._needs_repeated:
                    self._cycle_status = CycleStatus.FOUND
                    return
                else:
                    cycle_size = self._cycle_end - self._cycle_start + 1
                    self._cycle_start += cycle_size
                    self._cycle_end += cycle_size

    def _reset(self):
        self._cycle_status = CycleStatus.UNKNOWN
        self._testing_index = None
        self._cycle_start = None
        self._cycle_end = None
        self._repeat_count = 0
