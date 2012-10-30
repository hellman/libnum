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
*  randint\_bits(size) - random number with a given bit size
*  extract\_prime\_power(a, p) - s,t such that a = p**s * t
*  nroot(x, n) - truncated n'th root of x
*  gcd(a, b, ...) - greatest common divisor of all arguments
*  lcm(a, b, ...) - least common multiplier of all arguments
*  xgcd(a, b) - Extented Euclid GCD algorithm, returns (x, y, g) : a * x + b * y = gcd(a, b) = g

<b>Modular</b>

*  has\_invmod(a, n) - checks if a has modulo inverse
*  invmod(a, n) - modulo inverse
*  solve\_crt(remainders, modules) - solve Chinese Remainder Theoreme
*  factorial\_mod(n, factors) - compute factorial modulo composite number, needs factorization
*  nCk\_mod(n, k, factors) - compute combinations number modulo composite number, needs factorization
*  nCk\_mod\_prime\_power(n, k, p, e) - compute combinations number modulo prime power

<b>Modular square roots</b>

*  jacobi(a, b) - Jacobi symbol
*  has\_sqrtmod\_prime\_power(a, p, k) - checks if a number has modular square root, modulus is p**k
*  sqrtmod\_prime\_power(a, p, k) - modular square root by p**k
*  has\_sqrtmod(a, factors) - checks if a composite number has modular square root, needs factorization
*  sqrtmod(a, factors) - modular square root by a composite modulus, needs factorization

<b>Primes</b>

*  primes(n) - list of primes not greater than @n, slow method
*  factorize(n) - slow method of factorization
*  generate\_prime(size, k=25) - generates a pseudo-prime with @size bits length. @k is a number of tests.
*  generate\_prime\_from\_string(s, size=None, k=25) - generate a pseudo-prime starting with @s in string representation

<b>ECC</b>

*  Curve(a, b, p, g, order, cofactor, seed) - class for representing elliptic curve. Methods:
*   .is\_null(p) - checks if point is null
*   .is\_opposite(p1, p2) - checks if 2 points are opposite
*   .check(p) - checks if point is on the curve
*   .check\_x(x) - checks if there are points with given x on the curve (and returns them if any)
*   .find\_points\_in\_range(start, end) - list of points in range of x coordinate
*   .find\_points\_rand(count) - list of count random points
*   .add(p1, p2) - p1 + p2 on elliptic curve
*   .power(p, n) - n✕P or (P + P + ... + P) n times
*   .generate(n) - n✕G
*   .get\_order(p, limit) - slow method, trying to determine order of p; limit is max order to try

<b>Converting</b>

*  s2n(s) - packed string to number
*  n2s(n) - number to packed string
*  s2b(s) - packed string to binary string
*  b2s(b) - binary string to packed string

<b>Stuff</b>

*  grey\_code(n) - number in Grey code
*  rev\_grey\_code(g) - number from Grey code
*  nCk(n, k) - number of combinations
*  factorial(n) - factorial

About
---------------------

Author: hellman ( hellman1908@gmail.com )

License: GNU General Public License v2 (http://opensource.org/licenses/gpl-2.0.php)
