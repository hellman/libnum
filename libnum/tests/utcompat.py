# -*- coding:utf-8 -*-

"""
Functions to help in moving from unittest to pytest.
"""

import pytest
from collections import Counter


def assertEqual(a, b):
    assert a == b


def assertNotEqual(a, b):
    assert a != b


def assertTrue(expr):
    assert bool(expr) is True


def assertFalse(expr):
    assert bool(expr) is False


def assertIs(a, b):
    assert a is b


def assertIsNot(a, b):
    assert a is not b


def assertIsNone(expr):
    assert expr is None


def assertIsNotNone(expr):
    assert expr is not None


def assertIn(a, b):
    assert a in b


def assertNotIn(a, b):
    assert a not in b


def assertIsInstance(obj, cls):
    assert isinstance(obj, cls)


def assertNotIsInstance(obj, cls):
    assert not isinstance(obj, cls)


def assertRaises(exc, fun, *args, **kwargs):
    with pytest.raises(exc):
        fun(*args, **kwargs)

# TODO: implement assertRaisesRegex, assertWarns, assertWarnsRegex, and assertLogs


def assertAlmostEqual(a, b):
    assert round(a - b, 7) == 0


def assertNotAlmostEqual(a, b):
    assert round(a - b, 7) != 0


def assertGreater(a, b):
    assert a > b


def assertGreaterEqual(a, b):
    assert a >= b


def assertLess(a, b):
    assert a < b


def assertLessEqual(a, b):
    assert a <= b


def assertRegex(s, r):
    assert r.search(s)


def assertNotRegex(s, r):
    assert not r.search(s)


def assertCountEqual(a, b):
    # TODO: update to work with unhashable objects
    assertEqual(Counter(list(a)), Counter(list(b)))
