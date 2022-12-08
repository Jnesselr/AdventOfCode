import re
from dataclasses import dataclass, field
from queue import Queue
from typing import List, Optional

import typing

from aoc.util.inputs import Input


@dataclass
class FileEntry:
    name: str


@dataclass
class Directory(FileEntry):
    sub: List[FileEntry] = field(default_factory=lambda: [])

    @property
    def size(self) -> int:
        return sum(s.size for s in self.sub)


@dataclass
class File(FileEntry):
    size: int


class Y2022D7(object):
    cd_regex = re.compile(r'\$ cd (.*)')
    ls_regex = re.compile(r'\$ ls')
    dir_regex = re.compile(r'dir (.*)')
    file_regex = re.compile(r'(\d+) (.*)')

    def __init__(self, file_name):
        self._lines = Input(file_name).lines()

        self.root = Directory(name='/')
        cwd = self.root
        cwd_stack: List[Directory] = [cwd]

        for line in self._lines:
            if match := self.cd_regex.match(line):
                cwd_location = match.group(1)
                if cwd_location == '/':
                    cwd_stack = [self.root]
                elif cwd_location == '..':
                    cwd_stack.pop()
                else:
                    cwd = cwd_stack[-1]
                    for sub in cwd.sub:
                        if cwd_location == sub.name:
                            cwd_stack.append(typing.cast(Directory, sub))
                            break
                    else:
                        raise ValueError(f"Directory \"{cwd_location}\" not found!")
            elif self.ls_regex.match(line):
                pass
            elif match := self.dir_regex.match(line):
                to_add = Directory(
                    name=match.group(1)
                )
                cwd_stack[-1].sub.append(to_add)
            elif match := self.file_regex.match(line):
                to_add = File(
                    name=match.group(2),
                    size=int(match.group(1))
                )
                cwd_stack[-1].sub.append(to_add)
            else:
                raise ValueError(f"Unknown Regex: {line}")

    def part1(self):
        limit = 100000
        result = 0

        q = Queue()
        q.put(self.root)
        while not q.empty():
            d: Directory = q.get()
            for sub in d.sub:
                if isinstance(sub, Directory):
                    q.put(sub)

            if d.size <= limit:
                result += d.size

        print("Part 1:", result)

    def part2(self):

        total = 70000000
        total_needed = 30000000
        used = self.root.size
        unused = total - used
        wanted = total_needed - unused
        result = total

        q = Queue()
        q.put(self.root)
        while not q.empty():
            d: Directory = q.get()
            for sub in d.sub:
                if isinstance(sub, Directory):
                    q.put(sub)

            if d.size < wanted:
                continue  # Deleting it will do nothing

            if d.size < result:
                result = d.size

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2022D7("2022/7.txt")
    code.part1()
    code.part2()
