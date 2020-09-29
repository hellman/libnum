#-*- coding:utf-8 -*-

import pytest
import random

from functools import reduce
from itertools import combinations_with_replacement
from libnum import *
from libnum.compat import xrange
from utcompat import *


def test_has_invmod():
    for modulus in range(2, 1000, 31):
        for a in range(2, modulus, 5):
            if has_invmod(a, modulus):
                x = invmod(a, modulus)
                assertEqual((a * x) % modulus, 1)
            else:
                assertNotEqual(gcd(a, modulus), 1)
    assertRaises(ValueError, has_invmod, 1, 1)
    assertRaises(ValueError, has_invmod, 1, 0)
    assertRaises(ValueError, has_invmod, 1, -100)
    assertRaises(TypeError, has_invmod, "qwe", 10)
    assertRaises(TypeError, has_invmod, 10, "qwe")


def test_invmod():
    for modulus in range(3, 1001, 37):
        for a in range(2, modulus, 5):
            if has_invmod(a, modulus):
                x = invmod(a, modulus)
                assertEqual((a * x) % modulus, 1)
            else:
                assertRaises(ValueError, invmod, a, modulus)
    assertRaises(ValueError, invmod, 1, 1)
    assertRaises(ValueError, invmod, 1, 0)
    assertRaises(ValueError, invmod, 1, -100)
    assertRaises(TypeError, invmod, "qwe", 10)
    assertRaises(TypeError, invmod, 10, "qwe")


def test_euclid():
    for b in range(1, 1000, 13):
        for a in range(1, 1000, 7):
            g = gcd(a, b)
            x, y, g2 = xgcd(a, b)
            assertEqual(g, g2)
            assertEqual(a * x + b * y, g)
    assertEqual(xgcd(0, 10)[1:], (1, 10))
    assertEqual(xgcd(10, 0)[0::2], (1, 10))
    assertEqual(xgcd(0, 0)[2], 0)
    assertRaises(TypeError, xgcd, "qwe", 10)
    assertRaises(TypeError, xgcd, 10, "qwe")


def test_crt():
    for module in [2, 3, 5, 7, 1993]:
        for a in xrange(module):
            assertEqual(solve_crt([a], [module]), a)
            assertEqual(solve_crt([a, 0], [module, 1]), a)
    modules = [2, 3, 5, 19, 137]
    for i in xrange(1000):
        rems = []
        a = 7
        for m in modules:
            rems.append(a % m)
            a += 31337
        a = solve_crt(rems, modules)
        for i in xrange(len(modules)):
            assertEqual(rems[i], a % modules[i])
    assertRaises(TypeError, solve_crt, [1, 2, 3], [1, 2])
    assertRaises(ValueError, solve_crt, [], [])


def test_jacobi():

    def test_jacobi_prime(module):
        sqrs = set()
        for a in xrange(module):
           sqrs.add((a * a) % module)
        for a in xrange(module):
            if gcd(a, module) == 1:
                real = 1 if a in sqrs else -1
            else:
                real = 0
            test = jacobi(a, module)
            assertEqual(real, test)

    plist = primes(100) + [293, 1993, 2969, 2971, 9973, 11311]
    for module in plist[2:]:
        test_jacobi_prime(module)

    plist = primes(10)[2:]
    lezhs = {}

    for p in plist:
        lezhs[p] = [jacobi(a, p) for a in xrange(p)]

    for pnum in xrange(2, 4):
        for f in combinations_with_replacement(plist, pnum):
            n = reduce(operator.mul, f)
            for a in xrange(n):
                real = reduce(operator.mul, [lezhs[p][a % p] for p in f])
                test = jacobi(a, n)
                if real != test:
                    print("")
                    print("%d | %d %s" % (a, n, repr(f)))
                    print("Lezhandre symbols: %s" %
                          repr([lezhs[p][a % p] for p in f]))
                    for p in f:
                        print(lezhs[p])
                    print("real %s" % repr(real))
                    print("test %s" % repr(test))
                    print()
                assertEqual(real, test)

    assertRaises(ValueError, jacobi, 1, 2)
    assertRaises(ValueError, jacobi, 0, 6)
    assertRaises(ValueError, jacobi, 0, 0)
    assertRaises(Exception, jacobi, "qwe", 1024)
    assertRaises(Exception, jacobi, 123, "qwe")


def test_nCk_mod_pp():
    print("\nTesting nCk mod prime powers")
    for p, max_e in [(2, 8), (3, 4), (5, 3), (7, 3), (11, 2), (13, 2)]:
        print("    prime %s pow up to %s" % (repr(p), repr(max_e)))
        for i in xrange(100):
            k = random.randint(1, 10000)
            n = k + random.randint(0, 10000)
            e = random.randint(1, max_e)
            my = nCk_mod_prime_power(n, k, p, e)
            real = nCk(n, k) % (p ** e)
            assertEqual(my, real)


def test_nCk_mod():
    # TODO: do
    pass


def test_factorial_mod():
    print("\nTesting factorial mod prime powers")
    for p, max_e in [(2, 8), (3, 4), (5, 3), (7, 3), (11, 2)]:
        print("    prime %s pow up to %s" % (repr(p), repr(max_e)))
        for i in xrange(250):
            n = random.randint(1, 3000)
            e = random.randint(1, max_e)
            my = factorial_mod(n, {p: e})
            real = factorial(n) % (p ** e)
            assertEqual(my, real)

    print("\nTesting factorial mod small composites")
    for i in xrange(150):
        n = random.randint(1, 8000)
        x = random.randint(0, n * 2)
        my = factorial_mod(x, factorize(n))
        real = factorial(x) % n
        assertEqual(my, real)
