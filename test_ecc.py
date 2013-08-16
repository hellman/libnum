#!/usr/bin/env python
#-*- coding:utf-8 -*-

import unittest
from libnum import ecc


class TestECC(unittest.TestCase):
    def test_curve(self):
        NP = ecc.NULL_POINT
        c = ecc.Curve(1, 3, 7)

        points = [NP, (4, 1), (6, 6), (5, 0), (6, 1), (4, 6)]
        good = [(None, None), (4, 1), (6, 6), (5, 0), (6, 1), (4, 6),
                (4, 1), (6, 6), (5, 0), (6, 1), (4, 6), (None, None),
                (6, 6), (5, 0), (6, 1), (4, 6), (None, None), (4, 1),
                (5, 0), (6, 1), (4, 6), (None, None), (4, 1), (6, 6),
                (6, 1), (4, 6), (None, None), (4, 1), (6, 6), (5, 0),
                (4, 6), (None, None), (4, 1), (6, 6), (5, 0), (6, 1)]

        res = []
        for i in points:
            for j in points:
                res += [c.add(i, j)]

        self.assertEqual(res, good)

if __name__ == "__main__":
    unittest.main()
