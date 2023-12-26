from math import prod

from aoc.util.graph import Graph
from aoc.util.inputs import Input


class Y2023D25(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()

        self.graph: Graph[str] = Graph(directional=True)
        for line in lines:
            _from, _to_list = line.split(': ')
            for _to in _to_list.split(' '):
                self.graph.add(_from, _to)

        # self.graph.dotviz("out.dot")
        # neato -Tsvg out.dot -o out.svg
        # Manually found out that the edges that were bad were (hvm -- grd), (jmn -- zfk), and (pmn -- kdc)
        # I could have used an algorithm but graph partitioning is NP hard and while I could do it, sometimes
        # the best code is no code at all. :)

        self.graph.remove_node_link("hvm", "grd")
        self.graph.remove_node_link("grd", "hvm")
        self.graph.remove_node_link("jmn", "zfk")
        self.graph.remove_node_link("zfk", "jmn")
        self.graph.remove_node_link("pmn", "kdc")
        self.graph.remove_node_link("kdc", "pmn")

    def part1(self):
        result = prod(len(sep.all_nodes) for sep in self.graph.separate())

        print("Part 1:", result)


if __name__ == '__main__':
    code = Y2023D25("2023/25.txt")
    code.part1()
