#!/usr/bin/env python
#-*- coding:utf-8 -*-

import unittest
from libnum import *


class TestStuff(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
