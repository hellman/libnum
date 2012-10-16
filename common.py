#!/usr/bin/env python
#-*- coding:utf-8 -*-

import math
import random


def len_in_bits(n):
    """
    Return number of bits in binary representation of @n.
    """
    return math.trunc(math.log(n, 2)) + 1


def randint_bits(size):
    low = 1 << (size - 1)
    hi = (1 << size) - 1
    return random.randint(low, hi)


def nroot(x, n):
    """
    Return truncated n'th root of x.
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


def _gcd(a, b):
    """
    Return greatest common divisor using Euclid's Algorithm.
    """
    while b:
        a, b = b, a % b
    return abs(a)


def _lcm(a, b):
    """
    Return lowest common multiple.
    """
    if not a or not b:
        raise ZeroDivisionError("lcm arguments may not be zeros")
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
    return reduce(lambda a, b: _lcm(a, b), lst)


def xgcd(a, b):
    """
    Extented Euclid GCD algorithm.
    Return (x, y, g) : a * x + b * y = gcd(a, b) = g.
    """
    if a == 0:
        return 0, 1, b

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


def solve_linear(a, b, c):
    """
    Solve a*x + b*y = c.
    Solution (x0 + b*n, y0 + a*n).
    Return None or (x0, y0).
    """
    #TODO: do
    return None
