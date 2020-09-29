#-*- coding:utf-8 -*-

import pytest
from libnum import *
from libnum.compat import xrange
from utcompat import *


def test_grey_code():
    pg = 0
    for a in range(10000):
        g = grey_code(a)
        if a: # two consequent grey numbers differ only in one bit
            x = g ^ pg
            assertEqual(x ^ (x - 1), (x << 1) - 1)
        pg = g
        assertEqual(a, rev_grey_code(g))
    assertRaises(TypeError, grey_code, "qwe")


def test_nck():
    for n in (2, 5, 7, 100):
        csum = 0
        for x in xrange(n + 1):
            csum += nCk(n, x)
        assertEqual(csum, 2 ** n)

    row = [1]
    for n in xrange(1, 200):
        row = [0] + row + [0]
        row = [ row[i - 1] + row[i] for i in xrange(1, len(row)) ]
        for i in xrange(len(row)):
            assertEqual(row[i], nCk(n, i))

    assertEqual(nCk(10, -1), 0)
    assertEqual(nCk(10, 11), 0)
    assertEqual(nCk(0, 0), 1)
    assertEqual(nCk(0, 1), 0)
    assertRaises(ValueError, nCk, -1, 0)
