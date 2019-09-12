#-*- coding:utf-8 -*-

import pytest
from libnum import *
from utcompat import *


def test_s2n_n2s():
    s = "long string to test"
    val = 2418187513319072758194084480823884981773628276
    assertEqual(s2n(s), val)
    assertEqual(n2s(val), s)
    assertRaises(TypeError, s2n, 100)
    assertRaises(TypeError, n2s, "qwe")


def test_s2b_b2s():
    s = "just string"
    bs = "01101010011101010111001101110100001000000111"
    bs += "00110111010001110010011010010110111001100111"
    assertEqual(s2b(s), bs)
    assertEqual(b2s(bs), s)
    assertRaises(TypeError, s2b, 123)
    assertRaises(TypeError, b2s, 123)
    assertRaises(ValueError, b2s, "deadbeef")
