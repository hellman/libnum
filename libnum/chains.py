from libnum import nroot, gcd, Fraction


class Chain(object):
    def __init__(self, *args):
        self._chain = []
        self._frac = None
        if len(args) == 1:
            self.chain = args[0][::]
        else:
            a, b = args
            self.frac = Fraction(a, b)

    def _calcFrac(self):
        r = Fraction(0, 1)
        for x in reversed(self.chain):
            r = Fraction(1, x + r)
        return 1/r

    def _calcChain(self):
        r = []
        a, b = self.frac.numerator, self.frac.denominator
        while b != 1:
            r.append(a / b)
            a, b = b, a % b
        r.append(a)
        self._chain = r
        self._checkChain()
        return self._chain

    def _checkChain(self):
        if self._chain[-1] == 1:
            self._chain[-2] += 1
            self._chain = self._chain[:-1]
        return

    @property
    def frac(self):
        return self._frac

    @frac.setter
    def frac(self, f):
        self._frac = f
        self._chain = self._calcChain()

    @property
    def chain(self):
        return self._chain[::]

    @chain.setter
    def chain(self, c):
        self._chain = c
        self._checkChain()
        self._frac = self._calcFrac()

    @property
    def convergents(self):
        r1, r2 = 0, 1
        q1, q2 = 1, 0
        for c in self.chain:
            r1, r2, q1, q2 = q1, q2, c * q1 + r1, c * q2 + r2
            yield Fraction(q1, q2)


def sqrt_chained_fractions(n, limit=None):
    '''
    E.g. sqrt_chained_fractions(13) = [3,(1,1,1,1,6)]
    '''
    s = nroot(n, 2)
    if s**2 == n:
        return [s]
    res = []
    ps = 1, 0, 1
    seen = {ps: 0}
    while limit != 0:
        v, ps = _sqrt_iter(n, s, *ps)
        res.append(v)
        if ps in seen:
            pos = seen[ps]
            period = tuple(res[pos:])
            res = res[:pos]
            res.append(period)
            return res
        else:
            seen[ps] = len(res)

        if limit is not None:
            limit -= 1
    return res


def _sqrt_iter(n, s, t, a, b):
    '''
    take t*(sqrt(n)+a)/b
    s = floor(sqrt(n))
    return (v, next fraction params t, a, b)
    '''
    v = t * (s + a) // b
    t2 = b
    b2 = t * (n - (b * v - a)**2)
    a2 = b * v - a
    g = gcd(t2, b2)
    t2 //= g
    b2 //= g
    return v, (t2, a2, b2)


if __name__ == '__main__':
    for v in (2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 1337, 31337):
        print("sqrt(%d): %s" % (v, repr(sqrt_chained_fractions(v))))
