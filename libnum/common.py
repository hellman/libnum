import math
import random

from functools import reduce


def len_in_bits(n):
    """
    Return number of bits in binary representation of @n.
    Probably deprecated by .bit_length().
    """
    if not isinstance(n, int):
        raise TypeError("len_in_bits defined only for ints")
    return n.bit_length()


def randint_bits(size):
    return random.getrandbits(size) | (1 << (size - 1))


def ceil(x, y):
    """
    Divide x by y with ceiling.
    """
    return (x + y - 1) // y


def nroot(x, n):
    """
    Return truncated n'th root of x.
    Using binary search.
    """
    if n < 0:
        raise ValueError("can't extract negative root")

    if n == 0:
        raise ValueError("can't extract zero root")

    sign = 1
    if x < 0:
        sign = -1
        x = -x
        if n % 2 == 0:
            raise ValueError("can't extract even root of negative")

    high = 1
    while high ** n <= x:
        high <<= 1

    low = high >> 1
    while low < high:
        mid = (low + high) >> 1
        if low < mid and mid ** n < x:
            low = mid
        elif high > mid and mid ** n > x:
            high = mid
        else:
            return sign * mid
    return sign * (mid + 1)


_gcd = math.gcd


def _lcm(a, b):
    """
    Return lowest common multiple.
    """
    if not a or not b:
        return 0
    return abs(a * b) // _gcd(a, b)


def gcd(*lst):
    """
    Return gcd of a variable number of arguments.
    """
    return abs(reduce(lambda a, b: _gcd(a, b), lst))


def lcm(*lst):
    """
    Return lcm of a variable number of arguments.
    """
    return abs(reduce(lambda a, b: _lcm(a, b), lst))


def xgcd(a, b):
    """
    Extented Euclid GCD algorithm.
    Return (x, y, g) : a * x + b * y = gcd(a, b) = g.
    """
    if a == 0:
        return 0, 1, b
    if b == 0:
        return 1, 0, a

    px, ppx = 0, 1
    py, ppy = 1, 0

    while b:
        q = a // b
        a, b = b, a % b
        x = ppx - q * px
        y = ppy - q * py
        ppx, px = px, x
        ppy, py = py, y

    return ppx, ppy, a


def extract_prime_power(a, p):
    """
    Return s, t such that  a = p**s * t,  t % p = 0
    """
    s = 0
    if p > 2:
        while a and a % p == 0:
            s += 1
            a //= p
    elif p == 2:
        while a and a & 1 == 0:
            s += 1
            a >>= 1
    else:
        raise ValueError("Number %d is not a prime (is smaller than 2)" % p)
    return s, a
