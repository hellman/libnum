#-*- coding:utf-8 -*-
"""
libnum - Python library for some numbers functions:
  - working with primes (generating, primality tests)
  - common maths (gcd, lcm, modulo inverse, Jacobi symbol, sqrt)
  - elliptic curve cryptography functions
"""

from .primes import *
from .factorize import *
from .common import *
from .modular import *
from .sqrtmod import *
from .stuff import *
from .chains import *
from . import ecc


# be careful when changing this name, don't use test*!
def runtests():
    """
    Run all libnum tests and print output.
    """
    import os.path
    from inspect import getsourcefile
    from .tests import runtests as tests
    testdir = os.path.dirname(os.path.abspath(getsourcefile(tests)))
    importdir = os.path.abspath(testdir + "/../..")
    tests.testit(importdir, testdir)

# TODO: Add doctest after we have better docs
