#!/usr/bin/env python
#-*- coding:utf-8 -*-

from fractions import Fraction


class Chain(object):
	def __init__(self, *args):
		self._chain = []
		self._frac = None
		if len(args) == 1:
			self.chain = args[0][::]
		else:
			a, b = args
			self.frac = Fraction(a, b)

	def _calcFrac(self):
		r = Fraction(0, 1)
		for x in reversed(self.chain):
			r = Fraction(1, x + r)
		return 1/r

	def _calcChain(self):
		r = []
		a, b = self.frac.numerator, self.frac.denominator
		while b != 1:
			r.append(a / b)
			a, b = b, a % b
		r.append(a)
		self._chain = r
		self._checkChain()
		return self._chain

	def _checkChain(self):
		if self._chain[-1] == 1:
			self._chain[-2] += 1
			self._chain = self._chain[:-1]
		return

	@property
	def frac(self):
		return self._frac

	@frac.setter
	def frac(self, f):
		self._frac = f
		self._chain = self._calcChain()

	@property
	def chain(self):
		return self._chain[::]

	@chain.setter
	def chain(self, c):
		self._chain = c
		self._checkChain()
		self._frac = self._calcFrac()