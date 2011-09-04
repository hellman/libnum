#!/usr/bin/env python
#-*- coding:utf-8 -*-

from .primes import *
from .common import *
from .modular import *
from .stuff import *

def banner():
    print "libnum - Python library for some numbers functions:"
    print "  - working with primes (generating, primality tests)"
    print "  - common maths (gcd, lcm, inverse, Jacobi symbol, sqrt)"
    print

if __name__ == "__main__":
    banner()
