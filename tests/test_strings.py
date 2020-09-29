import pytest
from libnum import s2n, n2s, s2b, b2s


def test_s2n_n2s():
    s = b"long string to test"
    val = 2418187513319072758194084480823884981773628276
    assert s2n(s) == val
    assert n2s(val) == s
    with pytest.raises(TypeError):
        s2n(100)
    with pytest.raises(TypeError):
        n2s("qwe")


def test_s2b_b2s():
    s = b"just string"
    bs = "01101010011101010111001101110100001000000111"
    bs += "00110111010001110010011010010110111001100111"
    assert s2b(s) == bs
    assert b2s(bs) == s
    with pytest.raises(TypeError):
        s2b(123)
    with pytest.raises(TypeError):
        b2s(123)
    with pytest.raises(ValueError):
        b2s(b"deadbeef")
