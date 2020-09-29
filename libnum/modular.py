import operator

from functools import reduce

from .common import gcd, xgcd
from .stuff import factorial_get_prime_pow, factorial


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
    Solve Chinese Remainder Theorem.
    @modules and @remainders are lists.
    @modules must be pairwise coprimes.
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
        if module == 1:
            continue

        Ni = N // module
        b = invmod(Ni, module)

        x += remainders[i] * Ni * b
    return x % N


def nCk_mod(n, k, factors):
    """
    Compute nCk modulo, factorization of modulus is needed
    """
    rems = []
    mods = []
    for p, e in factors.items():
        rems.append(nCk_mod_prime_power(n, k, p, e))
        mods.append(p ** e)
    return solve_crt(rems, mods)


def factorial_mod(n, factors):
    """
    Compute factorial modulo, factorization of modulus is needed
    """
    rems = []
    mods = []
    for p, e in factors.items():
        pe = p ** e
        if n >= pe or factorial_get_prime_pow(n, p) >= e:
            factmod = 0
        else:
            factmod = factorial(n) % pe
        rems.append(factmod)
        mods.append(pe)
    return solve_crt(rems, mods)


def nCk_mod_prime_power(n, k, p, e):
    """
    Compute nCk mod small prime power: p**e
    Algorithm by Andrew Granville:
        http://www.dms.umontreal.ca/~andrew/PDF/BinCoeff.pdf
    What can be optimized:
        - compute (n-k)*(n-k+1)*...*n / 1*2*...*k instead of n!, k!, r!
        - ...
    """

    def nCk_get_prime_pow(n, k, p):
        res = factorial_get_prime_pow(n, p)
        res -= factorial_get_prime_pow(k, p)
        res -= factorial_get_prime_pow(n - k, p)
        return res

    def nCk_get_non_prime_part(n, k, p, e):
        pe = p ** e
        r = n - k

        fact_pe = [1]
        acc = 1
        for x in range(1, pe):
            if x % p == 0:
                x = 1
            acc = (acc * x) % pe
            fact_pe.append(acc)

        top = bottom = 1
        is_negative = 0
        digits = 0

        while n != 0:
            if acc != 1:
                if digits >= e:
                    is_negative ^= n & 1
                    is_negative ^= r & 1
                    is_negative ^= k & 1

            top = (top * fact_pe[n % pe]) % pe
            bottom = (bottom * fact_pe[r % pe]) % pe
            bottom = (bottom * fact_pe[k % pe]) % pe

            n //= p
            r //= p
            k //= p

            digits += 1

        res = (top * invmod(bottom, pe)) % pe
        if p != 2 or e < 3:
            if is_negative:
                res = pe - res
        return res

    prime_part_pow = nCk_get_prime_pow(n, k, p)
    if prime_part_pow >= e:
        return 0

    modpow = e - prime_part_pow

    r = nCk_get_non_prime_part(n, k, p, modpow) % (p ** modpow)
    return ((p ** prime_part_pow) * r) % (p ** e)
