#!/usr/bin/env python
#-*- coding:utf-8 -*-

import unittest
from libnum import *


class CommonMath(unittest.TestCase):
    def test_len_in_bits(self):
        self.assertEqual(len_in_bits(140737488355328), 48)
        self.assertEqual(len_in_bits(1023), 10)
        self.assertEqual(len_in_bits(1024), 11)
        self.assertEqual(len_in_bits(1), 1)
        self.assertEqual(len_in_bits(0), 0)

        # test number close to powers of two
        for p in (1, 10, 100, 1000, 10000, 100000):
            pow2 = 1 << p
            self.assertEqual(len_in_bits(pow2 + 1), p + 1)
            self.assertEqual(len_in_bits(pow2), p + 1)
            self.assertEqual(len_in_bits(pow2 - 1), p)

        self.assertRaises(TypeError, len_in_bits, "qwe")

    def test_nroot(self):
        for x in range(0, 100):
            for p in range(1, 3):
                n = x ** p
                self.assertEqual(nroot(n, p), x)

        self.assertEqual(nroot(-64, 3), -4)
        self.assertEqual(nroot(100, 2), 10)
        self.assertEqual(nroot(999, 3), 9)
        self.assertEqual(nroot(1000, 3), 10)
        self.assertEqual(nroot(1001, 3), 10)

        self.assertRaises(ValueError, nroot, 100, -1)
        self.assertRaises(ValueError, nroot, -100, 4)
        self.assertRaises(ValueError, nroot, 1, 0)
        self.assertRaises(TypeError, nroot, "qwe")

    def test_gcd_pair(self):
        self.assertEqual(gcd(100, 75), 25)
        self.assertEqual(gcd(-10, 155), 5)
        self.assertEqual(gcd(30, -77), 1)
        self.assertEqual(gcd(0, -77), 77)
        self.assertEqual(gcd(0, 0), 0)
        self.assertEqual(gcd(13, 0), 13)
        self.assertEqual(gcd(0, 13), 13)
        self.assertRaises(TypeError, gcd, "qwe", 10)
        self.assertRaises(TypeError, gcd, 10, "qwe")

    def test_gcd_list(self):
        self.assertEqual(gcd(100, 75, 150, -325), 25)
        self.assertEqual(gcd(-10, -155, -50), 5)
        self.assertEqual(gcd(-13), 13)
        self.assertEqual(gcd(3, 0, 30), 3)
        self.assertRaises(TypeError, gcd, "qwe")

    def test_lcm_pair(self):
        self.assertEqual(lcm(100, 75), 300)
        self.assertEqual(lcm(1, 31), 31)
        self.assertEqual(lcm(2, 37), 74)

        self.assertRaises(ZeroDivisionError, lcm, 1, 0)
        self.assertRaises(ZeroDivisionError, lcm, 0, 1)
        self.assertRaises(TypeError, lcm, "qwe", 10)
        self.assertRaises(TypeError, lcm, 10, "qwe")

    def test_lcm_list(self):
        self.assertEqual(lcm(100, 75), 300)
        self.assertEqual(lcm(100500), 100500)
        self.assertEqual(lcm(10, 20, 30, 40, 5, 80), 240)

        self.assertRaises(ZeroDivisionError, lcm, 123, 0, 0)
        self.assertRaises(ZeroDivisionError, lcm, 0, 100, 123)
        self.assertRaises(TypeError, lcm, "qwe", 10)
        self.assertRaises(TypeError, lcm, 10, "qwe")


if __name__ == "__main__":
    unittest.main()
