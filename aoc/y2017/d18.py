import re
from queue import Queue
from typing import List, Union

from aoc.util.inputs import Input


class BaseCode(object):
    def __init__(self, program: List[str]):
        self.program = program
        self.registers = {}

        self.terminated = False
        self.ip = 0

    def run(self):
        while not self.terminated:
            if self.ip < 0 or self.ip >= len(self.program):
                self.terminated = True
                break

            line = self.program[self.ip]
            self.ip += 1
            if (matched := re.match(r'snd (\w+|-?\d+)', line)) is not None:
                register = matched.group(1)
                self.snd(register)
            elif (matched := re.match(r'set (\w+) (\w+|-?\d+)', line)) is not None:
                register = matched.group(1)
                value = matched.group(2)
                self[register] = value
            elif (matched := re.match(r'add (\w+) (\w+|-?\d+)', line)) is not None:
                register = matched.group(1)
                value = matched.group(2)
                self[register] += self[value]
            elif (matched := re.match(r'mul (\w+) (\w+|-?\d+)', line)) is not None:
                register = matched.group(1)
                value = matched.group(2)
                self[register] *= self[value]
            elif (matched := re.match(r'mod (\w+) (\w+|-?\d+)', line)) is not None:
                register = matched.group(1)
                value = matched.group(2)
                self[register] %= self[value]
            elif (matched := re.match(r'rcv (\w+)', line)) is not None:
                register = matched.group(1)
                should_stop_running = self.rcv(register)
                if should_stop_running:
                    return
            elif (matched := re.match(r'jgz (\w+) (\w+|-?\d+)', line)) is not None:
                register = matched.group(1)
                value = matched.group(2)

                if self[register] > 0:
                    self.ip += self[value] - 1
            else:
                raise ValueError(f"Unmatched line: {line}")

    def __getitem__(self, item: str) -> int:
        if isinstance(item, int):
            return item

        try:
            return int(item)
        except ValueError:
            return self.registers.setdefault(item, 0)

    def __setitem__(self, key: str, value: Union[str, int]):
        self.registers[key] = self[value]

    def snd(self, register: str):
        pass

    def rcv(self, register: str) -> bool:
        pass


class SoundCode(BaseCode):
    def __init__(self, program: List[str]):
        super().__init__(program)
        self.last_sound = 0

    def snd(self, register: str):
        self.last_sound = self[register]

    def rcv(self, register: str) -> bool:
        return self[register] != 0


class PairCode(BaseCode):
    def __init__(self, program: List[str], program_id):
        super().__init__(program)
        self.send_queue = Queue()
        self.receive_queue = Queue()
        self.registers['p'] = program_id
        self.waiting = False

    def snd(self, register: str):
        self.send_queue.put(self[register])

    def rcv(self, register: str) -> bool:
        if self.receive_queue.qsize() == 0:
            self.ip -= 1  # Queue was empty, we'll need to try this command again
            self.waiting = True
            return True

        self.registers[register] = self.receive_queue.get()
        self.waiting = False

        return False


class Y2017D18(object):
    def __init__(self, file_name):
        self.lines = Input(file_name).lines()

    def part1(self):
        sound_code = SoundCode(self.lines)
        sound_code.run()
        result = sound_code.last_sound

        print("Part 1:", result)

    def part2(self):
        a = PairCode(self.lines, 0)
        b = PairCode(self.lines, 1)

        a_sent = b_sent = 0

        while True:
            a.run()
            b.run()

            a_sent += self._transfer_queues(a.send_queue, b.receive_queue)
            b_sent += self._transfer_queues(b.send_queue, a.receive_queue)

            if a.receive_queue.qsize() == 0 and b.receive_queue.qsize() == 0 and a.waiting and b.waiting:
                break

        result = b_sent

        print("Part 2:", result)

    @staticmethod
    def _transfer_queues(sending: Queue, receiving: Queue) -> int:
        result = 0

        while not sending.empty():
            result += 1
            receiving.put(sending.get())

        return result


if __name__ == '__main__':
    code = Y2017D18("2017/18.txt")
    code.part1()
    code.part2()
