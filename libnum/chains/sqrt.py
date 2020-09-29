#-*- coding:utf-8 -*-

from libnum import nroot, gcd


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
        v, ps = sqrt_iter(n, s, *ps)
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


def sqrt_iter(n, s, t, a, b):
    '''
    take t*(sqrt(n)+a)/b
    s = floor(sqrt(n))
    return (v, next fraction params t, a, b)
    '''
    v = t * (s + a) / b
    t2 = b
    b2 = t * (n - (b * v - a)**2)
    a2 = b * v - a
    g = gcd(t2, b2)
    t2 /= g
    b2 /= g
    return v, (t2, a2, b2)


if __name__ == '__main__':
    for v in (2, 3, 5, 6, 7, 8, 10, 11, 12, 13):
        print("sqrt(%d): %s" % (v, repr(sqrt_chained_fractions(v))))
