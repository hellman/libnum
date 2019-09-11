#!/usr/bin/env python
#-*- coding:utf-8 -*-

import unittest

from libnum.compat import xrange
from libnum.primes import *


class PrimesTest(unittest.TestCase):
    def test_primes(self):
        p = primes(100000)
        self.assertEqual(p[0], 2)
        self.assertEqual(len(p), 9592)
        self.assertEqual(p[9591], 99991)  # 9592th prime number
        self.assertRaises(TypeError, primes, "")

        self.assertEqual(primes(-1), [])
        self.assertEqual(primes(1), [])
        self.assertRaises(TypeError, primes, 1000000, "fake")

    def test_genprime(self):
        for size in (2, 10, 64, 128, 129, 256):
            for ntry in xrange(10):
                p = generate_prime(size, k=25)
                self.assertEqual(len_in_bits(p), size)

                self.assertTrue(prime_test_ferma(p, k=25))
                self.assertTrue(prime_test_solovay_strassen(p, k=25))
                self.assertTrue(prime_test_miller_rabin(p, k=25))
                self.assertTrue(prime_test(p, k=25))

        self.assertRaises(ValueError, generate_prime, 1)
        self.assertRaises(TypeError, generate_prime, "")

    def test_genprime_str(self):
        begin = "preved medved \xde\xad\xbe\xef\x00\x00\x00\x00"
        n = generate_prime_from_string(begin)
        s = n2s(n)
        self.assertTrue(s.startswith(begin))
        self.assertTrue(prime_test(n, 25))

        self.assertRaises(TypeError, generate_prime_from_string, 31337)
        self.assertRaises(ValueError, generate_prime_from_string, "test", 8)
        self.assertRaises(ValueError, generate_prime_from_string, "test", -8)

    def do_test_prime_test(self, func):
        for p in (3, 1993, 17333, 1582541, 459167430810992879232575962113190418519):
            self.assertTrue(func(p, 50))

        for p in primes(1000):
            self.assertTrue(func(p, 50))

        for not_p in (4, 1994, 1995, 16231845893292108971):
            self.assertFalse(func(not_p, 50))

        self.assertRaises(TypeError, func, "test")

    def test_fermatest(self):
        return self.do_test_prime_test(prime_test_ferma)

    def test_solovay(self):
        return self.do_test_prime_test(prime_test_solovay_strassen)

    def test_miller(self):
        return self.do_test_prime_test(prime_test_miller_rabin)


if __name__ == "__main__":
    unittest.main()
