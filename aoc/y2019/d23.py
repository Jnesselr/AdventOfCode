from dataclasses import dataclass
from queue import Queue
from typing import Dict

from aoc.util.inputs import Input
from aoc.util.intcode import Intcode


@dataclass(frozen=True)
class Packet(object):
    x: int
    y: int


class Y2019D23(object):
    def __init__(self, file_name):
        self.NICs: Dict[int, Intcode] = {}
        self.queues: Dict[int, Queue] = {}
        for i in range(50):
            self.NICs[i] = Intcode(file_name)
            self.queues[i] = Queue()

        self.queues[255] = Queue()

    def part1(self):
        self._reset_network()
        self._run_network()
        queue = self.queues[255]
        if queue.empty():
            raise ValueError("Something screwed up")
        result = queue.get().y

        print("Part 1:", result)

    def part2(self):
        self._reset_network()
        seen_y_values = set()

        while True:
            self._run_network()
            queue = self.queues[255]
            last_packet = None

            while not queue.empty():
                last_packet = queue.get()

            if last_packet is None:
                raise ValueError("NAT didn't have packet")

            if last_packet.y in seen_y_values:
                result = last_packet.y
                break
            seen_y_values.add(last_packet.y)

            self.queues[0].put(last_packet)

        print("Part 2:", result)

    def _run_network(self):
        any_sent = True
        while any_sent:
            any_sent = False
            for i in range(50):
                queue = self.queues[i]
                nic = self.NICs[i]

                if nic.waiting_for_input:
                    if queue.empty():
                        nic.input(-1)
                    else:
                        packet = queue.get()
                        nic.input(packet.x)
                        nic.input(packet.y)
                        any_sent = True

                while nic.has_output:
                    address = nic.output()
                    x = nic.output()
                    y = nic.output()
                    self.queues[address].put(Packet(x, y))
                    any_sent = True

    def _reset_network(self):
        for i in range(50):
            nic = self.NICs[i]
            nic.reset()
            nic.run()
            nic.input(i)
        [q.queue.clear() for q in self.queues.values()]


if __name__ == '__main__':
    code = Y2019D23("2019/23.txt")
    code.part1()
    code.part2()
