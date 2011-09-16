#!/usr/bin/env python
#-*- coding:utf-8 -*-

from .modular import prime_sqrtmod, prime_has_sqrt, invmod

__all__ = ('NULL_POINT', 'Curve')

NULL_POINT = (None, None)

class Curve:
    def __init__(self, a, b, p, g=None,
                                 order=None,
                                 cofactor=None,
                                 seed=None):
        self.a = a
        self.b = b
        self.module = p

        self.g = g
        self.order = order
        self.cofactor = cofactor
        self.seed = seed
        self.points_count = None
        if self.cofactor == 1 and self.order is not None:
            self.points_count = self.order
        return None

    def is_null(self, p):
        """
        Check if a point is curve's null point
        """
        return p == NULL_POINT

    def is_opposite(self, p1, p2):
        """
        Check if one point is opposite to another (p1 == -p2)
        """
        x1, y1 = p1
        x2, y2 = p2
        return (x1 == x2 and y1 == -y2 % self.module)

    def check(self, p):
        """
        Check if point is on the curve
        """
        x, y = p
        if self.is_null(p):
            return True
        left = (y ** 2) % self.module
        right = self.right(x)
        return left == right

    def check_x(self, x):
        """
        Check if there is a point on the curve with given @x coordinate
        """
        if x > self.module or x < 0:
            raise ValueError("Value " + str(x) +
                             " is not in range [0; <modulus>]")
        a = self.right(x)
        n = self.module

        if not prime_has_sqrt(a, n):
            return False

        ys = prime_sqrtmod(a, n)
        return map(lambda y: (x, y), ys)

    def right(self, x):
        """
        Right part of the curve equation: x^3 + a*x + b (mod p)
        """
        return (x ** 3 + self.a * x + self.b) % self.module

    def find_points_in_range(self, start=0, end=None):
        """
        List of points in given range for x coordinate
        """
        points = []

        if end is None:
            end = self.module - 1

        for x in xrange(start, end + 1):
            p = self.check_x(x)
            if p == False:
                continue
            points.extend(p)

        return points

    def find_points_rand(self, number=1):
        """
        List of @number random points on the curve
        """
        points = []

        while len(points) < number:
            x = random.randint(0, self.module)
            p = self.check_x(x)
            if p == False:
                continue
            points.append(p)

        return points

    def add(self, p1, p2):
        """
        Sum of two points
        """
        if self.is_null(p1):
            return p2

        if self.is_null(p2):
            return p1

        if self.is_opposite(p1, p2):
            return NULL_POINT

        x1, y1 = p1
        x2, y2 = p2

        l = 0
        if x1 != x2:
            l = (y2 - y1) * invmod(x2 - x1, self.module)
        else:
            l = (3 * x1 ** 2 + self.a) * invmod(2 * y1, self.module)

        x = (l * l - x1 - x2) % self.module
        y = (l * (x1 - x) - y1) % self.module  # yes, it's that new x
        return (x, y)

    def power(self, p, n):
        """
        n✕P or (P + P + ... + P) n times
        """
        if n == 0 or self.is_null(p):
            return NULL_POINT

        res = NULL_POINT
        while n:
            if n & 1:
                res = self.add(res, p)
            p = self.add(p, p)
            n >>= 1
        return res

    def generate(self, n):
        """
        Too lazy to give self.g to self.power
        """
        return self.power(self.g, n)

    def get_order(self, p, limit=None):
        """
        Tries to calculate order of @p, returns None if @limit is reached
        (SLOW method)
        """
        order = 1
        res = p
        while not self.is_null(res):
            res = self.add(res, p)
            order += 1
            if limit is not None and order >= limit:
                return None
        return order
