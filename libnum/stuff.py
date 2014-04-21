#-*- coding:utf-8 -*-

import operator


def grey_code(n):
    return n ^ (n >> 1)


def rev_grey_code(g):
    n = 0
    while g:
        n ^= g
        g >>= 1
    return n


def factorial(n):
    res = 1
    while n > 1:
        res *= n
        n -= 1
    return res


def factorial_get_prime_pow(n, p):
    """
    Return power of prime @p in @n!
    """
    count = 0
    ppow = p
    while ppow <= n:
        count += n // ppow
        ppow *= p
    return count


def nCk(n, k):
    """
    Combinations number
    """
    if n < 0: raise ValueError("Invalid value for n: %s" % n)
    if k < 0 or k > n: return 0
    if k in (0, n): return 1
    if k in (1, n-1): return n

    low_min = 1
    low_max = min(n, k)
    high_min = max(1, n - k + 1)
    high_max = n
    return reduce(operator.mul, range(high_min, high_max + 1), 1) / reduce(operator.mul, range(low_min, low_max + 1), 1)
