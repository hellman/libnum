import pytest
import random
import operator

from functools import reduce
from itertools import combinations_with_replacement
from libnum.common import gcd, xgcd
from libnum.primes import primes
from libnum.factorize import factorize
from libnum.stuff import factorial, nCk
from libnum.sqrtmod import jacobi
from libnum.modular import (
    has_invmod, invmod,
    nCk_mod_prime_power,
    factorial_mod,
    solve_crt,
)


def test_has_invmod():
    for modulus in range(2, 1000, 31):
        for a in range(2, modulus, 5):
            if has_invmod(a, modulus):
                x = invmod(a, modulus)
                assert (a * x) % modulus == 1
            else:
                assert gcd(a, modulus) != 1
    with pytest.raises(ValueError):
        has_invmod(1, 1)
    with pytest.raises(ValueError):
        has_invmod(1, 0)
    with pytest.raises(ValueError):
        has_invmod(1, -100)
    with pytest.raises(TypeError):
        has_invmod("qwe", 10)
    with pytest.raises(TypeError):
        has_invmod(10, "qwe")


def test_invmod():
    for modulus in range(3, 1001, 37):
        for a in range(2, modulus, 5):
            if has_invmod(a, modulus):
                x = invmod(a, modulus)
                assert (a * x) % modulus == 1
            else:
                with pytest.raises(ValueError):
                    invmod(a, modulus)
    with pytest.raises(ValueError):
        invmod(1, 1)
    with pytest.raises(ValueError):
        invmod(1, 0)
    with pytest.raises(ValueError):
        invmod(1, -100)
    with pytest.raises(TypeError):
        invmod("qwe", 10)
    with pytest.raises(TypeError):
        invmod(10, "qwe")


def test_euclid():
    for b in range(1, 1000, 13):
        for a in range(1, 1000, 7):
            g = gcd(a, b)
            x, y, g2 = xgcd(a, b)
            assert g == g2
            assert a * x + b * y == g
    assert xgcd(0, 10)[1:] == (1, 10)
    assert xgcd(10, 0)[0::2] == (1, 10)
    assert xgcd(0, 0)[2] == 0
    with pytest.raises(TypeError):
        xgcd("qwe", 10)
    with pytest.raises(TypeError):
        xgcd(10, "qwe")


def test_crt():
    for module in [2, 3, 5, 7, 1993]:
        for a in range(module):
            assert solve_crt([a], [module]) == a
            assert solve_crt([a, 0], [module, 1]) == a
    modules = [2, 3, 5, 19, 137]
    for i in range(1000):
        rems = []
        a = 7
        for m in modules:
            rems.append(a % m)
            a += 31337
        a = solve_crt(rems, modules)
        for i in range(len(modules)):
            assert rems[i] == a % modules[i]
    with pytest.raises(TypeError):
        solve_crt([1, 2, 3], [1, 2])
    with pytest.raises(ValueError):
        solve_crt([], [])


def test_jacobi():

    def test_jacobi_prime(module):
        sqrs = set()
        for a in range(module):
            sqrs.add((a * a) % module)
        for a in range(module):
            if gcd(a, module) == 1:
                real = 1 if a in sqrs else -1
            else:
                real = 0
            test = jacobi(a, module)
            assert real == test

    plist = primes(100) + [293, 1993, 2969, 2971, 9973, 11311]
    for module in plist[2:]:
        test_jacobi_prime(module)

    plist = primes(10)[2:]
    lezhs = {}

    for p in plist:
        lezhs[p] = [jacobi(a, p) for a in range(p)]

    for pnum in range(2, 4):
        for f in combinations_with_replacement(plist, pnum):
            n = reduce(operator.mul, f)
            for a in range(n):
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
                assert real == test

    with pytest.raises(ValueError):
        jacobi(1, 2)
    with pytest.raises(ValueError):
        jacobi(0, 6)
    with pytest.raises(ValueError):
        jacobi(0, 0)
    with pytest.raises(Exception):
        jacobi("qwe", 1024)
    with pytest.raises(Exception):
        jacobi(123, "qwe")


def test_nCk_mod_pp():
    print("\nTesting nCk mod prime powers")
    for p, max_e in [(2, 8), (3, 4), (5, 3), (7, 3), (11, 2), (13, 2)]:
        print("    prime %s pow up to %s" % (repr(p), repr(max_e)))
        for i in range(100):
            k = random.randint(1, 10000)
            n = k + random.randint(0, 10000)
            e = random.randint(1, max_e)
            my = nCk_mod_prime_power(n, k, p, e)
            real = nCk(n, k) % (p ** e)
            assert my == real


def test_nCk_mod():
    # TODO: do
    pass


def test_factorial_mod():
    print("\nTesting factorial mod prime powers")
    for p, max_e in [(2, 8), (3, 4), (5, 3), (7, 3), (11, 2)]:
        print("    prime %s pow up to %s" % (repr(p), repr(max_e)))
        for i in range(250):
            n = random.randint(1, 3000)
            e = random.randint(1, max_e)
            my = factorial_mod(n, {p: e})
            real = factorial(n) % (p ** e)
            assert my == real

    print("\nTesting factorial mod small composites")
    for i in range(150):
        n = random.randint(1, 8000)
        x = random.randint(0, n * 2)
        my = factorial_mod(x, factorize(n))
        real = factorial(x) % n
        assert my == real
