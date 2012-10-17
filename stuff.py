#!/usr/bin/env python
#-*- coding:utf-8 -*-

import operator


def grey_code(n):
    return n ^ (n >> 1)


def rev_grey_code(g):
    n = 0
    while g:
        n ^= g
        g >>= 1
    return n


def nCk(n, k):
    """
    Combinations number.
    """
    return int(round(
        reduce(operator.mul, (float(n-i)/(i+1) for i in range(k)), 1)
    ))