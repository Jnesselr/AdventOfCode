from functools import reduce


from math import gcd


class ChineseRemainderTheorem(object):
    """
    Reference code used to ensure correctness:
    https://rosettacode.org/wiki/Chinese_remainder_theorem#Python

    Understandable math: https://crypto.stanford.edu/pbc/notes/numbertheory/crt.html
    """
    def __init__(self):
        self._n = []
        self._a = []

    @property
    def result(self):
        _sum = 0
        _product = reduce(lambda x, y: x * y, self._n)
        for a, n in zip(self._a, self._n):
            p = _product // n
            _sum += a * p * self._modulo_inverse(p, n)

        return _sum % _product

    def a_mod_n(self, a, n):
        if len(list(filter(lambda x: gcd(x, n) != 1, self._n))) > 0:
            raise ValueError(f"Elements are not pairwise coprime")
        self._n.append(n)
        self._a.append(a)

    @staticmethod
    def _modulo_inverse(p, n):
        original_n = n
        x0, x1 = 0, 1
        if n == 1:
            return 1
        while p > 1:
            q = p // n
            p, n = n, p % n
            x0, x1 = x1 - q * x0, x0
        if x1 < 0:
            x1 += original_n
        return x1
