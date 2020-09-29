import random
import pytest

from libnum.common import gcd, randint_bits
from libnum.primes import generate_prime
from libnum.sqrtmod import (
    sqrtmod, sqrtmod_prime_power,
    has_sqrtmod, has_sqrtmod_prime_power,
    jacobi,
)
from libnum.factorize import factorize, unfactorize


def check_valid_sqrt_pp(x, a, p, k):
    check_jacobi(a, p ** k, 1)

    all_roots = list(sqrtmod_prime_power(a, p, k))
    assert all_roots
    assert sorted(all_roots) == sorted(set(all_roots))

    reduced_roots = map(lambda a: a % p ** k, all_roots)
    assert sorted(all_roots) == sorted(reduced_roots)

    for r in all_roots:
        assert pow(r, 2, p ** k) == a

    if x is not None:
        assert x in all_roots


def check_valid_sqrt_composite(x, a, factors):
    n = unfactorize(factors)

    all_roots = list(sqrtmod(a, factors))
    assert all_roots
    assert sorted(all_roots) == sorted(set(all_roots))

    for r in all_roots:
        assert pow(r, 2, n) == a

    if x is not None:
        assert x in all_roots


def check_jacobi(a, n, has_sqrt):
    if n & 1 == 0:
        return
    j = jacobi(a, n)
    if gcd(a, n) != 1:
        assert j == 0
    elif has_sqrt:
        assert j == 1
    else:
        assert j


def test_has_sqrtmod():
    with pytest.raises(TypeError):
        has_sqrtmod_prime_power(3, 9, "")
    with pytest.raises(TypeError):
        has_sqrtmod_prime_power(3, "", 30)
    with pytest.raises(TypeError):
        has_sqrtmod_prime_power("", 9, 30)
    with pytest.raises(ValueError):
        has_sqrtmod_prime_power(1, 2, 0)  # 1 mod 2**0
    with pytest.raises(ValueError):
        has_sqrtmod_prime_power(1, 1, 2)  # 1 mod 1**2

    with pytest.raises(TypeError):
        has_sqrtmod(3, {9: ""})
    with pytest.raises(TypeError):
        has_sqrtmod(3, {"": 2})
    with pytest.raises(TypeError):
        has_sqrtmod("", {9: 30})
    with pytest.raises(TypeError):
        has_sqrtmod("", {(9,): 30})
    with pytest.raises(ValueError):
        has_sqrtmod(1, {2: 0})  # 1 mod 2**0
    with pytest.raises(ValueError):
        has_sqrtmod(1, {1: 2})  # 1 mod 1**2
    with pytest.raises(ValueError):
        has_sqrtmod(3, {})


def test_sqrt_pp_all():
    print("\nTesting all residues by small modules")
    pairs = [(2, 11), (3, 7), (5, 5), (7, 4), (11, 3), (13, 3), (97, 2)]
    for prime, maxpow in pairs:
        for k in range(1, maxpow + 1):
            n = prime ** k
            print("    Testing %s**%s" % (prime, k))
            for x in range(n):
                a = pow(x, 2, n)

                is_sqrt = has_sqrtmod(a, {prime: k})
                is_sqrt2 = has_sqrtmod_prime_power(a, prime, k)
                assert is_sqrt == is_sqrt2
                if is_sqrt:
                    check_valid_sqrt_pp(None, a, prime, k)

                check_jacobi(a, n, is_sqrt)

                assert has_sqrtmod_prime_power(a, prime, k)
                assert has_sqrtmod(a, {prime: k})
                check_valid_sqrt_pp(x, a, prime, k)


def test_sqrt_pp_rand():
    print("\nTesting random residues by random modules")
    pairs = [(2, 500), (10, 100), (64, 15), (128, 5), (129, 5), (256, 2)]
    for size, maxpow in pairs:
        for i in range(10):
            p = generate_prime(size, k=25)
            print("    Testing %s-bit prime with max power %s: %s..." %
                  (size, maxpow, str(p)[:32]))
            for j in range(10):
                k = random.randint(1, maxpow)
                x = random.randint(0, p ** k - 1)
                a = pow(x, 2, p ** k)
                check_valid_sqrt_pp(x, a, p, k)


def test_sqrt_composite_all():
    print("\nTesting all residues by small composite modules")
    ns = [
        10, 30, 50, 99, 100, 655, 1025, 1337,
        7 ** 3 * 3, 2 ** 6 * 13, 2 ** 4 * 3 ** 3 * 5, 3 * 3 * 5 * 7,
        1024,
    ]
    for n in ns:
        f = factorize(n)
        print("    Testing %s = %s" % (n, f))
        for x in range(n):
            a = pow(x, 2, n)
            is_sqrt = has_sqrtmod(a, f)
            if is_sqrt:
                check_valid_sqrt_composite(None, a, f)

            check_jacobi(a, n, is_sqrt)

            assert has_sqrtmod(a, f)
            check_valid_sqrt_composite(x, a, f)


def test_sqrt_composite_rand():
    print("\nTesting all residues by random composite modules")
    for size, ntries in [(2, 2), (3, 3), (5, 10), (7, 20), (10, 20)]:
        for i in range(ntries):
            n = randint_bits(size)
            f = factorize(n)
            print("    Testing %s-bit number: %s..." %
                  (size, str(n)[:32]))
            for x in range(n):
                a = pow(x, 2, n)
                is_sqrt = has_sqrtmod(a, f)
                if is_sqrt:
                    check_valid_sqrt_composite(None, a, f)

                check_jacobi(a, n, is_sqrt)

                assert has_sqrtmod(a, f)
                check_valid_sqrt_composite(x, a, f)


def test_sqrt_composite_rand_rand():
    print("\nTesting random residues by random composite modules")
    for size, ntries in [(10, 20), (20, 20), (24, 20), (30, 20)]:
        for i in range(ntries):
            n = randint_bits(size)
            f = factorize(n)
            print("    Testing %s-bit number: %s..." %
                  (size, str(n)[:32]))
            for j in range(30):
                x = random.randint(0, n - 1)
                a = pow(x, 2, n)
                is_sqrt = has_sqrtmod(a, f)
                if is_sqrt:
                    check_valid_sqrt_composite(None, a, f)

                check_jacobi(a, n, is_sqrt)

                assert has_sqrtmod(a, f)
                check_valid_sqrt_composite(x, a, f)
