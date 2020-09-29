import pytest
from libnum import len_in_bits, gcd, lcm, nroot


def test_len_in_bits():
    assert len_in_bits(140737488355328) == 48
    assert len_in_bits(1023) == 10
    assert len_in_bits(1024) == 11
    assert len_in_bits(1) == 1
    assert len_in_bits(0) == 0

    # test number close to powers of two
    for p in (1, 10, 100, 1000, 10000, 100000):
        pow2 = 1 << p
        assert len_in_bits(pow2 + 1), p == 1
        assert len_in_bits(pow2), p == 1
        assert len_in_bits(pow2 - 1) == p

    with pytest.raises(TypeError):
        len_in_bits("qwe")


def test_nroot():
    for x in range(0, 100):
        for p in range(1, 3):
            n = x ** p
            assert nroot(n, p) == x

    assert nroot(-64, 3) == -4
    assert nroot(100, 2) == 10
    assert nroot(999, 3) == 9
    assert nroot(1000, 3) == 10
    assert nroot(1001, 3) == 10

    with pytest.raises(ValueError):
        nroot(100, -1)
    with pytest.raises(ValueError):
        nroot(-100, 4)
    with pytest.raises(ValueError):
        nroot(1, 0)
    with pytest.raises(TypeError):
        nroot("qwe")


def test_gcd_pair():
    assert gcd(100, 75) == 25
    assert gcd(-10, 155) == 5
    assert gcd(30, -77) == 1
    assert gcd(0, -77) == 77
    assert gcd(0, 0) == 0
    assert gcd(13, 0) == 13
    assert gcd(0, 13) == 13
    with pytest.raises(TypeError):
        gcd("qwe", 10)
    with pytest.raises(TypeError):
        gcd(10, "qwe")


def test_gcd_list():
    assert gcd(100, 75, 150, -325) == 25
    assert gcd(-10, -155, -50) == 5
    assert gcd(-13) == 13
    assert gcd(3, 0, 30) == 3
    with pytest.raises(TypeError):
        gcd("qwe")


def test_lcm_pair():
    assert lcm(100, 75) == 300
    assert lcm(1, 31) == 31
    assert lcm(2, 37) == 74

    assert lcm(1, 0) == 0
    assert lcm(0, 1) == 0

    with pytest.raises(TypeError):
        lcm("qwe", 10)
    with pytest.raises(TypeError):
        lcm(10, "qwe")


def test_lcm_list():
    assert lcm(100, 75) == 300
    assert lcm(100500) == 100500
    assert lcm(10, 20, 30, 40, 5, 80) == 240

    assert lcm(123, 0, 0) == 0
    assert lcm(0, 100, 123) == 0

    with pytest.raises(TypeError):
        lcm("qwe", 10)
    with pytest.raises(TypeError):
        lcm(10, "qwe")
