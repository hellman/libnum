#!/usr/bin/env python
#-*- coding:utf-8 -*-

import unittest
from libnum import *
from libnum.compat import xrange


class StuffTest(unittest.TestCase):
    def test_grey_code(self):
        pg = 0
        for a in range(10000):
            g = grey_code(a)
            if a:  # two consequent grey numbers differ only in one bit
                x = g ^ pg
                self.assertEqual(x ^ (x - 1), (x << 1) - 1)
            pg = g
            self.assertEqual(a, rev_grey_code(g))
        self.assertRaises(TypeError, grey_code, "qwe")

    def test_nck(self):
        for n in (2, 5, 7, 100):
            csum = 0
            for x in xrange(n + 1):
                csum += nCk(n, x)
            self.assertEqual(csum, 2**n)

        row = [1]
        for n in xrange(1, 200):
            row = [0] + row + [0]
            row = [ row[i-1] + row[i] for i in xrange(1, len(row)) ]
            for i in xrange(len(row)):
                self.assertEqual(row[i], nCk(n, i))

        self.assertEqual(nCk(10, -1), 0)
        self.assertEqual(nCk(10, 11), 0)
        self.assertEqual(nCk(0, 0), 1)
        self.assertEqual(nCk(0, 1), 0)
        self.assertRaises(ValueError, nCk, -1, 0)


if __name__ == "__main__":
    unittest.main()
