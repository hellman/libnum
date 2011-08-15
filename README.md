libnum
====================

This is a python library for some numbers functions:

*  working with primes (generating, primality tests)
*  common maths (gcd, lcm, n'th root)
*  modular arithmetics (inverse, Jacobi symbol, square root, solve CRT)
*  converting strings to numbers or binary strings

List of functions
---------------------

<b>Common maths</b>

*  len\_in\_bits(n) - number of bits in binary representation of @n
*  nroot(x, n) - truncated n'th root of x
*  gcd(a, b, ...) - greatest common divisor of all arguments
*  lcm(a, b, ...) - least common multiplier of all arguments
*  xgcd(a, b) - Extented Euclid GCD algorithm, returns (x, y, g) : a * x + b * y = gcd(a, b) = g

<b>Modular</b>

*  has\_invmod(a, n) - checks if a has modulo inverse
*  invmod(a, n) - modulo inverse
*  jacobi(a, b) - Jacobi symbol
*  prime\_has\_sqrt(a, p) - checks if a number has modular square root, modulus must be prime
*  prime\_sqrtmod(p, b) - modular square root, modulus must be prime
*  has\_sqrt(a, factors) - checks if a complex number has modular square root, needs factorization
*  sqrtmod(a, factors) - modular square root by a complex modulus, needs factorization, also all prime factors must have power 1 (no squares, cubes, etc.)
*  solve\_crt(remainders, modules) - solve Chinese Remainder Theoreme

<b>Primes</b>

*  primes(n) - list of primes not greater than @n, slow method
*  factorize(n) - slow method of factorization
*  generate\_prime(size, k=25) - generates a pseudo-prime with @size bits length. @k is a number of tests.
*  generate\_prime\_from\_string(s, size=None, k=25) - generate a pseudo-prime starting with @s in string representation

<b>Converting</b>

*  s2n(s) - packed string to number
*  n2s(n) - number to packed string
*  s2b(s) - packed string to binary string
*  b2s(b) - binary string to packed string

<b>Stuff</b>

*  grey\_code(n) - number in Grey code
*  rev\_grey\_code(g) - number from Grey code
*  nCk(n, k) - number of combinations

About
---------------------

Author: hellman ( hellman1908@gmail.com )

License: GNU General Public License v2 (http://opensource.org/licenses/gpl-2.0.php)
