#!/usr/bin/env python
#-*- coding:utf-8 -*-

import random
import operator

from .common import *


def has_invmod(a, modulus):
    """
    Check if @a can be inversed under @modulus.
    Call this before calling invmod.
    """
    if modulus < 2:
        raise ValueError("modulus must be greater than 1")

    if a == 0 or gcd(a, modulus) != 1:
        return False
    else:
        return True


def invmod(a, n):
    """
    Return 1 / a (mod n).
    @a and @n must be co-primes.
    """
    if n < 2:
        raise ValueError("modulus must be greater than 1")

    x, y, g = xgcd(a, n)

    if g != 1:
        raise ValueError("no invmod for given @a and @n")
    else:
        return x % n


def solve_crt(remainders, modules):
    """
    Solve Chinese Remainder Theoreme.
    @modules and @remainders are lists.
    @modules must be pairwsise coprimes.
    """
    if len(modules) != len(remainders):
        raise TypeError("modules and remainders lists must have same len")

    if len(modules) == 0:
        raise ValueError("Empty lists are given")

    if len(modules) == 1:
        return remainders[0]

    x = 0
    N = reduce(operator.mul, modules)
    for i, module in enumerate(modules):
        Ni = N // module
        b = invmod(Ni, module)
        x += remainders[i] * Ni * b
    return x % N