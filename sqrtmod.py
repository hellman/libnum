#!/usr/bin/env python
#-*- coding:utf-8 -*-

import operator
from itertools import product

from .common import *
from .modular import *


def has_sqrtmod(a, factors=None):
    """
    Check if @a is quadratic residue, factorization needed
    @factors - list of (prime, power) tuples
    """
    if not factors:
        raise ValueError("Factors list can't be empty: %s" % factors)

    for p, k in factors:
        if p <= 1 or k <= 0:
            raise ValueError("Not valid prime power: %s**%s" % (p, k))

        if has_sqrtmod_prime_power(a, p, k) == False:
            return False
    return True


def sqrtmod(a, factors):
    """
    x ^ 2 = a (mod *factors).
    Yield square roots by product of @factors as modulus.
    @factors - list of (prime, power) tuples
    """
    coprime_factors = [p ** k for p, k in factors]
    n = reduce(operator.mul, coprime_factors)

    sqrts = []
    for i, (p, k) in enumerate(factors):
        # it's bad that all roots by each modulus are calculated here
        # - we can start yielding roots faster
        sqrts.append( list(sqrtmod_prime_power(a % coprime_factors[i], p, k) ) )

    for rems in product(*sqrts):
        yield solve_crt(rems, coprime_factors) 
    return


def has_sqrtmod_prime_power(a, p, n=1):
    """
    Check if @a (mod @p**@n) is quadratic residue, @p is prime.
    """
    if p < 2:
        raise ValueError("Prime must be greater than 1: " + str(p))

    if n < 1:
        raise ValueError("Prime power must be positive: " + str(n))

    a = a % (p ** n)

    if a in (0, 1):
        return True
    
    e, a = extract_prime_power(a, p)

    if e:
        if e & 1:
            return False
        else:
            return has_sqrtmod_prime_power(a, p, n)

    if p == 2:  # power of 2
        return a % 8 == 1
    return jacobi(a, p) == 1


def sqrtmod_prime_power(a, p, k=1):
    """
    Yield square roots of @a mod @p**@k,
    @p - prime
    @k >= 1
    """
    if k < 1:
        raise ValueError("prime power k < 1: %d" % k)

    powers = [1]
    pow_p = 1
    for i in xrange(k):
        pow_p *= p
        powers.append(pow_p)

    # x**2 == a (mod p),  p is prime
    def sqrtmod_prime(a, p):
        if a == 0:
            return (0,)
        if a == 1:
            return (1, p-1) if p != 2 else (1,)

        if jacobi(a, p) == -1:
            raise ValueError("No square root for %d (mod %d)" % (a, p))

        while True:
            b = random.randint(1, p - 1)
            if jacobi(b, p) == -1:
                break

        pow2, t = extract_prime_power(p - 1, 2)
        ai = invmod(a, p)

        c = pow(b, t, p)
        r = pow(a, (t + 1) // 2, p)
        for i in range(1, pow2):
            e = pow(2, pow2 - i - 1, p - 1)
            d = pow(pow(r, 2, p) * ai, e, p)
            if d == p - 1:
                r = (r * c) % p
            c = pow(c, 2, p)
        return (r, (-r) % p)  # both roots

    # x**2 == a (mod p**k),  p is prime,  gcd(a, p) == 1
    def sqrtmod_prime_power_for_coprime(a, p, k):
        if a == 1:
            if p == 2:
                if k == 1: return (1, )
                if k == 2: return (1, 3)
                if k == 3: return (1, 3, 5, 7)
            else:
                return 1, pow_p - 1

        if p == 2:  # roots mod 2**k
            roots = 1, 3
            powind = 3
            while powind < k:
                next_powind = powind + 1
                next_roots = set()

                for r in roots:
                    if pow(r, 2, powers[next_powind]) == a % powers[next_powind]:
                        next_roots.add(r)

                    r = powers[powind] - r
                    if pow(r, 2, powers[next_powind]) == a % powers[next_powind]:
                        next_roots.add(r)

                powind = next_powind
                roots = next_roots

            roots = [pow_p - r for r in roots] + list(roots)
            return roots

        else:  # p >= 3
            r = sqrtmod_prime(a, p)[0]  # any root
            powind = 1
            while powind < k:
                next_powind = min(powind * 2, k)
                # Represent root:  x = +- (r  +  p**powind * t1)
                b = (a - r**2) % powers[next_powind]
                b = (b * invmod( 2*r, powers[next_powind] )) % powers[next_powind]
                if b:
                    if b % powers[powind]:
                        raise ValueError("No square root for given value")
                    b /= powers[powind]
                    b %= powers[powind]
                    # Represent  t1 = t2 * p**powind + b
                    # Re-represent root: x = +- [ (r + p**powind * b)  +  t2 * p**(powind*2)  ]
                    r += powers[powind] * b
                powind = next_powind
                # For next round: x = +- (r  +  t2 * p**next_powind)
            return r % pow_p, (-r) % pow_p
        return

    # x**2 == 0 (mod p**k),  p is prime
    def sqrt_for_zero(p, k):
        roots = [0]
        start_k = (k / 2 + 1) if k & 1 else (k / 2)

        r = powers[start_k] % pow_p
        r0 = r
        while True:
            if r:  # don't duplicate zero
                roots.append(r)
            r = (r + powers[start_k]) % pow_p
            if r == r0:
                break
        return roots

    # main code

    if a == 0:
        for r in sqrt_for_zero(p, k):
            yield r
        return

    e, a = extract_prime_power(a, p)

    if e & 1:
        raise ValueError("No square root for %d (mod %d**%d)" % (a, p, k))

    p_acc = powers[e >> 1]
    sqrt_k = k - e

    roots = sqrtmod_prime_power_for_coprime(a, p, sqrt_k)

    if sqrt_k == 0:
        for r in roots:
            yield (r * p_acc) % pow_p
        return

    all_roots = set()
    for r in roots:
        r0 = r % pow_p
        while True:
            root = (r * p_acc) % pow_p
            if root not in all_roots:
                yield root
                all_roots.add(root)
            r = (r + powers[sqrt_k]) % pow_p
            if r == r0:
                break
    return


def jacobi(a, n):
    """
    Return Jacobi symbol (or Legendre symbol if n is prime)
    """
    s = 1
    while True:
        if n < 1: raise ValueError("Too small module for Jacobi symbol: " + str(n))
        if n & 1 == 0: raise ValueError("Jacobi is defined only for odd modules")
        if n == 1: return s
        a = a % n
        if a == 0: return 0
        if a == 1: return s

        if a & 1 == 0:
            if n % 8 in (3, 5):
                s = -s
            a >>= 1
            continue

        if a % 4 == 3 and n % 4 == 3:
            s = -s

        a, n = n, a
    return