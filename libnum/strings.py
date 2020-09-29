def s2n(s):
    """
    String to number.
    """
    if not len(s):
        return 0
    try:
        enc = s.encode("hex")
    except LookupError:
        enc = "".join("%02x" % ord(c) for c in s)
    return int(enc, 16)


def n2s(n):
    """
    Number to string.
    """
    s = hex(n)[2:].rstrip("L")
    if len(s) % 2 != 0:
        s = "0" + s
    try:
        return s.decode("hex")
    except AttributeError:
        return "".join(chr(int(s[i:i + 2], 16)) for i in range(0, len(s), 2))


def s2b(s):
    """
    String to binary.
    """
    res = bin(s2n(s))[2:]
    return "0" * ((8 - len(res)) % 8) + res


def b2s(b):
    """
    Binary to string.
    """
    return n2s(int(b, 2))
