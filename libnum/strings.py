from .common import len_in_bits


def s2n(s):
    r"""
    String to number (big endian).

    >>> s2n("BA")  # 0x4241
    16961
    >>> s2n(b'\x01\x00')
    256
    """
    if isinstance(s, str):
        s = s.encode("utf-8")
    return int.from_bytes(s, "big")


def n2s(n):
    r"""
    Number to string (big endian).

    >>> n2s(0x4241)
    b'BA'
    >>> n2s(0x100)
    b'\x01\x00'
    """
    nbits = len_in_bits(n)
    nbytes = (nbits + 7) >> 3
    return n.to_bytes(nbytes, "big")


def s2b(s):
    """
    String to binary.

    >>> s2b("qwe")
    '011100010111011101100101'
    """
    res = bin(s2n(s))[2:]
    return "0" * ((8 - len(res)) % 8) + res


def b2s(b):
    """
    Binary to string.

    >>> b2s("011100010111011101100101")
    b'qwe'
    """
    return n2s(int(b, 2))
