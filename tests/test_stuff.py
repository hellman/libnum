import pytest
from libnum import grey_code, rev_grey_code, nCk


def test_grey_code():
    pg = 0
    for a in range(10000):
        g = grey_code(a)
        if a:  # two consequent grey numbers differ only in one bit
            x = g ^ pg
            assert x ^ (x - 1) == (x << 1) - 1
        pg = g
        assert a == rev_grey_code(g)
    with pytest.raises(TypeError):
        grey_code("qwe")


def test_nck():
    for n in (2, 5, 7, 100):
        csum = 0
        for x in range(n + 1):
            csum += nCk(n, x)
        assert csum == 2 ** n

    row = [1]
    for n in range(1, 200):
        row = [0] + row + [0]
        row = [row[i - 1] + row[i] for i in range(1, len(row))]
        for i in range(len(row)):
            assert row[i] == nCk(n, i)

    assert nCk(10, -1) == 0
    assert nCk(10, 11) == 0
    assert nCk(0, 0) == 1
    assert nCk(0, 1) == 0
    with pytest.raises(ValueError):
        nCk(-1, 0)
