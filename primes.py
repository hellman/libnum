#!/usr/bin/env python
#-*- coding:utf-8 -*-

import math
import random
import operator
from .common import *
from .strings import *

_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
_small_primes_product = 1
_primes_bits = [[] for i in range(11)]
_primes_mask = []


def _init():
    global _small_primes_product, _primes, _primes_bits, _primes_mask
    _primes = primes(1024)
    for p in _primes:
        _primes_bits[len_in_bits(p)].append(p)
    _small_primes_product = reduce(operator.mul, _primes)
    _primes_mask = [(x in _primes) for x in xrange(_primes[-1] + 1)]
    return


def primes(until, method=None):
    """
    Return list of primes not greater than @until. Rather slow.
    """
    global _primes, _primes_mask

    if until < 2:
        return []

    if until <= _primes[-1]:
        for index, prime in enumerate(_primes):
            if prime > until:
                return _primes[:index]

    if method is None:
        for i in xrange(_primes[-1] + 2, until + 1, 2):
            sqrt = math.sqrt(i) + 1
            for j in _primes:
                if i % j == 0:
                    break
                if j > sqrt:
                    _primes.append(i)
                    break
            else:
                _primes.append(i)
    elif method.lower().startswith("erato"):
        limit = nroot(until, 2) + 1
        if len(_primes_mask) < until + 1:
            _primes_mask.extend([True] * ((until + 1 - len(_primes_mask))))
        
        _primes_mask[0] = False
        _primes_mask[1] = False

        _primes = []
        for i in range(2, until + 1):
            if not _primes_mask[i]:
                continue
            _primes.append(i)
            for j in range(i * 2, until + 1, i):
                _primes_mask[j] = False
    else:
        raise TypeError("Unknown method: %s" % method)    
    return _primes
    

def factorize(n):
    """
    Return list of @n's factors. Slowest method.
    """
    if n < 1:
        raise ValueError("factorize() accepts only numbers greater than 1 (" +
                         "given: " + str(n) + ")")
    if n == 1:
        return [1]

    limit = int(math.sqrt(n)) + 1

    fact = []
    plist = primes(limit)

    for p in plist:
        while n % p == 0:
            fact.append(p)
            n = n // p
        if n == 1:
            return fact
        if n in plist:
            return fact + [n]

    if n != 1:
        return fact + [n]
    else:
        return fact


def generate_prime(size, k=25):
    """
    Generate a pseudo-prime with @size bits length.
    Optional arg @k=25 defines number of tests.
    """
    if size < 2:
        raise ValueError("No primes smaller than 2 bits!")

    if size <= 10:
        return random.choice(_primes_bits[size])

    low = 1 << (size - 1)
    hi = (1 << size) - 1

    while True:
        n = random.randint(low, hi) | 1  # only odd

        if gcd(_small_primes_product, n) != 1:
            continue

        if ferma_test(n, k):
            return n
    return


def generate_prime_from_string(s, size=None, k=25):
    """
    Generate a pseudo-prime starting with @s in string representation.
    Optional arg @size defines length in bits, if is not set than +some bytes.
    Optional arg @k=25 defines number of tests.
    """
    if not size:
        if len(s) > 512:
            size = len(s) * 8 + 32
        else:
            size = len(s) * 8 + 16

    if len(s) * 8 >= size:
        raise ValueError("given size is smaller than string length")

    if size % 8:
        raise ValueError("size must be 8*n")

    extend_len = size - len(s) * 8

    visible_part = s2n(s) << extend_len
    hi = 2 ** extend_len

    while True:
        n = visible_part | random.randint(1, hi) | 1  # only even

        if gcd(_small_primes_product, n) != 1:
            continue

        if ferma_test(n, k):
            return n
    return


def ferma_test(p, k=25):
    """
    Test for primality based on Ferma's Little Theorem.
    """
    if p < 2:
        return False

    if p <= 3:
        return True

    for j in xrange(k):
        a = random.randint(2, p - 1)
        result = pow(a, p - 1, p)
        if result != 1:
            return False

    return True


#def ferma_test_hi(p, k=25):
#    m = p - 1
#    s = 0
#    while not m & 1:
#        s = s + 1
#        m = m >> 1
#
#    # if a ^ m % n != 1 then not a prime
#    # else do test again (k times)
#    for j in range(k):
#        a = random.randint(2, p - 1)
#        b = pow(a, m, p)
#        if b == 1:
#            continue
#        for i in range(1, s):
#            if b == p - 1:
#                return True
#            b = (b*b) % p
#        break
#    return False

_init()
