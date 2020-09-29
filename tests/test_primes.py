import pytest

from libnum.primes import (
    primes,
    prime_test,
    prime_test_ferma,
    prime_test_solovay_strassen,
    prime_test_miller_rabin,
    generate_prime,
    generate_prime_from_string,
)
from libnum import len_in_bits, n2s


def test_primes():
    p = primes(100000)
    assert p[0] == 2
    assert len(p) == 9592
    assert p[9591] == 99991  # 9592th prime number
    with pytest.raises(TypeError):
        primes("")

    assert primes(-1) == []
    assert primes(1) == []
    with pytest.raises(TypeError):
        primes(1000000, "fake")


def test_genprime():
    for size in (2, 10, 64, 128, 129, 256):
        for ntry in range(10):
            p = generate_prime(size, k=25)
            assert len_in_bits(p) == size

            assert prime_test_ferma(p, k=25)
            assert prime_test_solovay_strassen(p, k=25)
            assert prime_test_miller_rabin(p, k=25)
            assert prime_test(p, k=25)

    with pytest.raises(ValueError):
        generate_prime(1)
    with pytest.raises(TypeError):
        generate_prime("")


def test_genprime_str():
    begin = b"preved medved \xde\xad\xbe\xef\x00\x00\x00\x00"
    n = generate_prime_from_string(begin)
    s = n2s(n)
    assert s.startswith(begin)
    assert prime_test(n, 25)

    with pytest.raises(TypeError):
        generate_prime_from_string(31337)
    with pytest.raises(ValueError):
        generate_prime_from_string("test", 8)
    with pytest.raises(ValueError):
        generate_prime_from_string("test", -8)


def do_test_prime_test(func):
    for p in (3, 1993, 17333, 1582541, 459167430810992879232575962113190418519):
        assert func(p, 50)

    for p in primes(1000):
        assert func(p, 50)

    for not_p in (4, 1994, 1995, 16231845893292108971):
        assert not func(not_p, 50)

    with pytest.raises(TypeError):
        func("test")


def test_fermatest():
    return do_test_prime_test(prime_test_ferma)


def test_solovay():
    return do_test_prime_test(prime_test_solovay_strassen)


def test_miller():
    return do_test_prime_test(prime_test_miller_rabin)
