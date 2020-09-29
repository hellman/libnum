#-*- coding:utf-8 -*-

import pytest
from libnum import *
from utcompat import *


def test_len_in_bits():
    assertEqual(len_in_bits(140737488355328), 48)
    assertEqual(len_in_bits(1023), 10)
    assertEqual(len_in_bits(1024), 11)
    assertEqual(len_in_bits(1), 1)
    assertEqual(len_in_bits(0), 0)

    # test number close to powers of two
    for p in (1, 10, 100, 1000, 10000, 100000):
        pow2 = 1 << p
        assertEqual(len_in_bits(pow2 + 1), p + 1)
        assertEqual(len_in_bits(pow2), p + 1)
        assertEqual(len_in_bits(pow2 - 1), p)

    assertRaises(TypeError, len_in_bits, "qwe")


def test_nroot():
    for x in range(0, 100):
        for p in range(1, 3):
            n = x ** p
            assertEqual(nroot(n, p), x)

    assertEqual(nroot(-64, 3), -4)
    assertEqual(nroot(100, 2), 10)
    assertEqual(nroot(999, 3), 9)
    assertEqual(nroot(1000, 3), 10)
    assertEqual(nroot(1001, 3), 10)

    assertRaises(ValueError, nroot, 100, -1)
    assertRaises(ValueError, nroot, -100, 4)
    assertRaises(ValueError, nroot, 1, 0)
    assertRaises(TypeError, nroot, "qwe")


def test_gcd_pair():
    assertEqual(gcd(100, 75), 25)
    assertEqual(gcd(-10, 155), 5)
    assertEqual(gcd(30, -77), 1)
    assertEqual(gcd(0, -77), 77)
    assertEqual(gcd(0, 0), 0)
    assertEqual(gcd(13, 0), 13)
    assertEqual(gcd(0, 13), 13)
    assertRaises(TypeError, gcd, "qwe", 10)
    assertRaises(TypeError, gcd, 10, "qwe")


def test_gcd_list():
    assertEqual(gcd(100, 75, 150, -325), 25)
    assertEqual(gcd(-10, -155, -50), 5)
    assertEqual(gcd(-13), 13)
    assertEqual(gcd(3, 0, 30), 3)
    assertRaises(TypeError, gcd, "qwe")


def test_lcm_pair():
    assertEqual(lcm(100, 75), 300)
    assertEqual(lcm(1, 31), 31)
    assertEqual(lcm(2, 37), 74)

    assertRaises(ZeroDivisionError, lcm, 1, 0)
    assertRaises(ZeroDivisionError, lcm, 0, 1)
    assertRaises(TypeError, lcm, "qwe", 10)
    assertRaises(TypeError, lcm, 10, "qwe")


def test_lcm_list():
    assertEqual(lcm(100, 75), 300)
    assertEqual(lcm(100500), 100500)
    assertEqual(lcm(10, 20, 30, 40, 5, 80), 240)

    assertRaises(ZeroDivisionError, lcm, 123, 0, 0)
    assertRaises(ZeroDivisionError, lcm, 0, 100, 123)
    assertRaises(TypeError, lcm, "qwe", 10)
    assertRaises(TypeError, lcm, 10, "qwe")
