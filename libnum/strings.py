#-*- coding:utf-8 -*-


def s2n(s):
    """
    String to number.
    """
    if not len(s):
        return 0
    try:
        enc = s.encode("hex")
    except LookupError:
        enc = s.encode("utf-8").hex()
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
        return bytes.fromhex(s).decode("utf-8")


def s2b(s):
    """
    String to binary.
    """
    ret = []
    for c in s:
        ret.append(bin(ord(c))[2:].zfill(8))
    return "".join(ret)


def b2s(b):
    """
    Binary to string.
    """
    ret = []
    b = b.zfill(((len(b) + 7) // 8) * 8)
    for pos in range(0, len(b), 8):
        ret.append(chr(int(b[pos:pos + 8], 2)))
    return "".join(ret)
