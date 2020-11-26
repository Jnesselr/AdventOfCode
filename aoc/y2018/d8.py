from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from queue import Queue
from typing import List, Dict

from aoc.util.inputs import Input


@dataclass(frozen=True)
class TreeNode(object):
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)
    children: List[TreeNode] = field(default_factory=lambda: [], hash=False)
    metadata: List[int] = field(default_factory=lambda: [], hash=False)


class Y2018D8(object):
    def __init__(self, file_name):
        line = Input(file_name).line()
        self._root = self._make_tree(iter(line.split(' ')))

    @classmethod
    def _make_tree(cls, iterator) -> TreeNode:
        node_count = int(next(iterator))
        metadata_count = int(next(iterator))

        children = []
        for _ in range(node_count):
            children.append(cls._make_tree(iterator))

        metadata = []
        for _ in range(metadata_count):
            metadata.append(int(next(iterator)))

        return TreeNode(
            children=children,
            metadata=metadata
        )

    def part1(self):
        queue: Queue = Queue()
        queue.put(self._root)

        result = 0
        while not queue.empty():
            node = queue.get()
            result += sum(node.metadata)

            for child in node.children:
                queue.put(child)

        print("Part 1:", result)

    def part2(self):
        scores: Dict[TreeNode, int] = {}

        def _get_score(node: TreeNode):
            if node in scores:
                return scores[node]

            score = 0

            if len(node.children) == 0:
                score = sum(node.metadata)
            else:
                for index in node.metadata:
                    if index > len(node.children):
                        continue

                    score += _get_score(node.children[index - 1])

            scores[node] = score
            return score

        result = _get_score(self._root)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2018D8("2018/8.txt")
    code.part1()
    code.part2()

