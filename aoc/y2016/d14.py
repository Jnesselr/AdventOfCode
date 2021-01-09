import hashlib

from aoc.util.inputs import Input


class KeyGenerator(object):
    def __init__(self, salt, key_stretching=False):
        self.salt = salt
        self.key_stretching = key_stretching

        self._hashes = {}

        self.keys = []
        key_gen = self._key_generator()
        for i in range(64):
            self.keys.append(next(key_gen))

    @property
    def last_index(self):
        return [index for index, key in self._hashes.items() if key == self.keys[-1]].pop()

    def _hash(self, index: int):
        if index not in self._hashes:
            md5_hex = hashlib.md5(f'{self.salt}{index}'.encode()).hexdigest()

            if self.key_stretching:
                for i in range(2016):
                    md5_hex = hashlib.md5(md5_hex.encode()).hexdigest()

            self._hashes[index] = md5_hex

        return self._hashes[index]

    def _key_generator(self):
        index = 0
        while True:
            md5_hash = self._hash(index)

            search_term = None
            for i in range(len(md5_hash) - 2):
                if md5_hash[i] == md5_hash[i + 1] == md5_hash[i + 2]:
                    search_term = md5_hash[i] * 5
                    break

            if search_term is not None:
                for i in range(index + 1, index + 1001):
                    new_hash = self._hash(i)
                    if search_term in new_hash:
                        yield md5_hash
                        break
            index += 1


class Y2016D14(object):
    def __init__(self, file_name):
        self.salt = Input(file_name).line()

    def part1(self):
        key_generator = KeyGenerator(self.salt)
        result = key_generator.last_index

        print("Part 1:", result)

    def part2(self):
        key_generator = KeyGenerator(self.salt, key_stretching=True)
        result = key_generator.last_index

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2016D14("2016/14.txt")
    code.part1()
    code.part2()
