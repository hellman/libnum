#!/usr/bin/env python
#-*- coding:utf-8 -*-

import unittest
import random

from libnum.primes import *
from libnum.sqrtmod import *
from libnum.factorize import factorize, unfactorize


class SqrtTest(unittest.TestCase):
    def check_valid_sqrt_pp(self, x, a, p, k):
        self.check_jacobi(a, p**k, 1)

        any_root = sqrtmod_prime_power(a, p, k).next()
        self.assertEqual(pow(any_root, 2, p**k), a)

        all_roots = list(sqrtmod_prime_power(a, p, k))
        self.assertEqual(sorted(all_roots), sorted(set(all_roots)))

        reduced_roots = map(lambda a: a % p**k, all_roots)
        self.assertEqual(sorted(all_roots), sorted(reduced_roots))

        for r in all_roots:
            self.assertEqual(pow(r, 2, p**k), a)

        if x is not None:
            self.assertTrue(x in all_roots)

    def check_valid_sqrt_composite(self, x, a, factors):
        n = unfactorize(factors)

        any_root = sqrtmod(a, factors).next()
        self.assertEqual(pow(any_root, 2, n), a)

        all_roots = list(sqrtmod(a, factors))
        self.assertEqual(sorted(all_roots), sorted(set(all_roots)))

        for r in all_roots:
            self.assertEqual(pow(r, 2, n), a)

        if x is not None:
            self.assertTrue(x in all_roots)

    def check_jacobi(self, a, n, has_sqrt):
        if n & 1 == 0: return
        j = jacobi(a, n)
        if gcd(a, n) != 1: self.assertEqual(j, 0)
        elif has_sqrt: self.assertEqual(j, 1)
        else: self.assertTrue(j != 0)

    def test_has_sqrtmod(self):
        self.assertRaises(TypeError, has_sqrtmod_prime_power, 3, 9, "")
        self.assertRaises(TypeError, has_sqrtmod_prime_power, 3, "", 30)
        self.assertRaises(TypeError, has_sqrtmod_prime_power, "", 9, 30)
        self.assertRaises(ValueError, has_sqrtmod_prime_power, 1, 2, 0)  # 1 mod 2**0
        self.assertRaises(ValueError, has_sqrtmod_prime_power, 1, 1, 2)  # 1 mod 1**2

        self.assertRaises(TypeError, has_sqrtmod, 3, {9: ""})
        self.assertRaises(TypeError, has_sqrtmod, 3, {"": 2})
        self.assertRaises(TypeError, has_sqrtmod, "", {9: 30})
        self.assertRaises(TypeError, has_sqrtmod, "", {(9,): 30})
        self.assertRaises(ValueError, has_sqrtmod, 1, {2: 0})  # 1 mod 2**0
        self.assertRaises(ValueError, has_sqrtmod, 1, {1: 2})  # 1 mod 1**2
        self.assertRaises(ValueError, has_sqrtmod, 3, {})

    def test_sqrt_pp_all(self):
        print "\nTesting all residues by small modules"
        for prime, maxpow in [(2, 11), (3, 7), (5, 5), (7, 4), (11, 3), (13, 3), (97, 2)]:
            for k in xrange(1, maxpow + 1):
                n = prime ** k
                print "    Testing %s**%s" % (prime, k)
                for x in xrange(n):
                    a = pow(x, 2, n)

                    is_sqrt = has_sqrtmod(a, {prime: k})
                    is_sqrt2 = has_sqrtmod_prime_power(a, prime, k)
                    self.assertEqual(is_sqrt, is_sqrt2)
                    if is_sqrt:
                        self.check_valid_sqrt_pp(None, a, prime, k)

                    self.check_jacobi(a, n, is_sqrt)

                    self.assertTrue( has_sqrtmod_prime_power(a, prime, k) )
                    self.assertTrue( has_sqrtmod(a, {prime: k}) )
                    self.check_valid_sqrt_pp(x, a, prime, k)

    def test_sqrt_pp_rand(self):
        print "\nTesting random residues by random modules"
        for size, maxpow in [(2, 500), (10, 100), (64, 15), (128, 5), (129, 5), (256, 2)]:
            for i in xrange(10):
                p = generate_prime(size, k=25)
                print "    Testing %s-bit prime with max power %s: %s..." % ( size, maxpow, str(p)[:32] )
                for j in xrange(10):
                    k = random.randint(1, maxpow)
                    x = random.randint(0, p**k - 1)
                    a = pow(x, 2, p**k)
                    self.check_valid_sqrt_pp(x, a, p, k)

    def test_sqrt_composite_all(self):
        print "\nTesting all residues by small composite modules"
        for n in [10, 30, 50, 99, 100, 655, 1025, 1337, 7**3 * 3, 2**6 * 13, 2**4 * 3 ** 3 * 5, 3 * 3 * 5 * 7, 1024]:
            f = factorize(n)
            print "    Testing %s = %s" % (n, f)
            for x in xrange(n):
                a = pow(x, 2, n)
                is_sqrt = has_sqrtmod(a, f)
                if is_sqrt:
                    self.check_valid_sqrt_composite(None, a, f)

                self.check_jacobi(a, n, is_sqrt)

                self.assertTrue( has_sqrtmod(a, f) )
                self.check_valid_sqrt_composite(x, a, f)

    def test_sqrt_composite_rand(self):
        print "\nTesting all residues by random composite modules"
        for size, ntries in [(2, 2), (3, 3), (5, 10), (7, 20), (10, 20)]:
            for i in xrange(ntries):
                n = randint_bits(size)
                f = factorize(n)
                print "    Testing %s-bit number: %s..." % ( size, str(n)[:32] )
                for x in xrange(n):
                    a = pow(x, 2, n)
                    is_sqrt = has_sqrtmod(a, f)
                    if is_sqrt:
                        self.check_valid_sqrt_composite(None, a, f)

                    self.check_jacobi(a, n, is_sqrt)

                    self.assertTrue( has_sqrtmod(a, f) )
                    self.check_valid_sqrt_composite(x, a, f)

    def test_sqrt_composite_rand_rand(self):
        print "\nTesting random residues by random composite modules"
        for size, ntries in [(10, 20), (20, 20), (24, 20), (30, 20)]:
            for i in xrange(ntries):
                n = randint_bits(size)
                f = factorize(n)
                print "    Testing %s-bit number: %s..." % ( size, str(n)[:32] )
                for j in xrange(30):
                    x = random.randint(0, n - 1)
                    a = pow(x, 2, n)
                    is_sqrt = has_sqrtmod(a, f)
                    if is_sqrt:
                        self.check_valid_sqrt_composite(None, a, f)

                    self.check_jacobi(a, n, is_sqrt)

                    self.assertTrue( has_sqrtmod(a, f) )
                    self.check_valid_sqrt_composite(x, a, f)


if __name__ == "__main__":
    unittest.main()
