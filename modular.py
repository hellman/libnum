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
    if a == 0:
        return False
    elif gcd(a, modulus) != 1:
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

    x, y, g = map(lambda x: x % n, xgcd(a, n))

    if g != 1:
        raise ValueError("no invmod for given @a and @n")
    else:
        return x


def jacobi(a, n):
    """
    Return Jacobi symbol (or Legendre symbol if n is prime)
    """
    if n < 1:
        raise ValueError("Too small module for Jacobi symbol: " + str(n))

    if a in [0, 1]:
        return a

    if gcd(a, n) != 1:
        return 0

    # n must be odd
    while n & 1 == 0:
        n >>= 1

    if n == 1:
        return 1

    a = a % n

    if a in [0, 1]:
        return a

    e = 0
    a1 = a
    while a1 and a1 % 2 == 0:
        a1 >>= 1
        e += 1

    if e % 2 == 0 or n % 8 in [1, 7]:
        s = 1
    elif n % 8 in [3, 5]:
        s = -1
    else:
        raise Exception("jacobi fail :(")

    if n % 4 == 3 and a1 % 4 == 3:
        s = -s

    if a1 == 1:
        return s
    else:
        return s * jacobi(n, a1)


def quadratic_residue(a, factors):
    """
    Check if @a is quadratic residue, factorization needed
    @factors - list of (prime, power) tuples
    """
    for p, e in factors:
        if prime_quadratic_residue(a, p, e) == False:
            return False
    return True


def prime_quadratic_residue(a, p, n=1):
    """
    Check if @a (mod @p^@n) is quadratic residue, @p is prime.
    """
    if p < 2:
        raise ValueError("Prime must be greater than 1: " + str(p))

    if n < 1:
        raise ValueError("Prime power must be positive: " + str(n))

    a = a % (p ** n)

    if a in [0, 1]:
        return True
    
    e = 0
    while a and a % p == 0:
        a //= p
        e += 1
    if e:
        if e & 1:
            # looks like it works
            return False  # * residue(a, p)
        else:
            return prime_quadratic_residue(a, p)

    if p == 2:  # power of 2
        if a % 8 == 1:
            return True
        else:
            return False
    return True if jacobi(a, p) == 1 else False    
    

def prime_has_sqrt(a, p):
    """
    Check if @a has modular square root, @p must be prime.
    """
    if a == 0:
        return True
    return (jacobi(a, p) == 1)


def prime_sqrtmod(a, p):
    """
    Return modular square root. Modulus must be prime.
    """
    s = 0
    t = p - 1

    if a == 0:
        return [0]
    if a == 1:
        return [1, p-1]

    if jacobi(a, p) == -1:
        raise ValueError("No square root for %d (mod %d)" % (a, p))

    while True:
        b = random.randint(1, p - 1)
        if jacobi(b, p) == -1:
            break

    while t & 1 == 0:
        s += 1
        t >>= 1

    ai = 0
    if a != 0:
        ai = invmod(a, p)

    c = pow(b, t, p)
    r = pow(a, (t + 1) // 2, p)
    for i in range(1, s):
        e = pow(2, s - i - 1, p)
        d = pow((r * r % p) * ai % p, e, p)
        if d == p - 1:
            r = r * c % p
        c = c * c % p

    if r:
        return [r, -r % p]  # both roots
    return [0]


def has_sqrt(a, factors):
    """
    Check if @a has modular square root,
    product of @factors is modulus.
    WARNING: There's a problem if any of the primes has power > 1
    """
    for p in factors:
        if jacobi(a, p) == -1:
            return False
    return True


def sqrtmod(a, factors):
    """
    x ^ 2 = a (mod *factors).
    Return square root by product of @factors as modulus.
    (Yeah, needs factorization).
    WARNING: There's a problem if any of the primes has power > 1
    """
    n = reduce(operator.mul, factors)

    powers = {}
    for p in factors:
        powers[p] = powers.get(p, 0) + 1

    factors = []
    for p in powers:
        factors.append(p ** powers[p])
    print "FACTORS", factors
    ss = map(lambda p: prime_sqrtmod(a % p, p), factors)
    roots = set()
    masks = [2 ** i for i in xrange(len(factors))]
    for sign_acc in xrange(0, 2 ** len(factors)):
        signs = [-1 if sign_acc & m else 1 for m in masks]
        rems = [signs[i] * ss[i] for i in xrange(len(ss))]
        #print rems
        #print factors, "\n"
        root = solve_crt(rems, factors)
        roots.add(root % n)
    print "ROOTS", roots
    print
    return list(roots)


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
    x = x % N
    return x
