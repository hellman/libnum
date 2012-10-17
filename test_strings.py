#!/usr/bin/env python
#-*- coding:utf-8 -*-

import unittest
from libnum import *


class StringsTest(unittest.TestCase):
    def test_s2n_n2s(self):
        s = "long string to test"
        val = 2418187513319072758194084480823884981773628276
        self.assertEqual(s2n(s), val)
        self.assertEqual(n2s(val), s)
        self.assertRaises(TypeError, s2n, 100)
        self.assertRaises(TypeError, n2s, "qwe")

    def test_s2b_b2s(self):
        s = "just string"
        bs = "01101010011101010111001101110100001000000111"
        bs += "00110111010001110010011010010110111001100111"
        self.assertEqual(s2b(s), bs)
        self.assertEqual(b2s(bs), s)
        self.assertRaises(TypeError, s2b, 123)
        self.assertRaises(TypeError, b2s, 123)
        self.assertRaises(ValueError, b2s, "deadbeef")


if __name__ == "__main__":
    unittest.main()
