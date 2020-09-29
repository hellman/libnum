#-*- coding:utf-8 -*-

import pytest
from libnum.ranges import Ranges


def test_Ranges():
    print("test")
    r = Ranges((0, 10))
    assert r.len == 11
    assert r.min == 0
    assert r.max == 10
    r.add_range(100, 200)
    assert r == Ranges((0, 10), (100, 200))
    assert r.len == 11 + 101
    assert r.min == 0
    assert r.max == 200
