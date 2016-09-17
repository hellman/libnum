#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
from distutils.core import setup

import libnum


setup(name='libnum',
      version=libnum.__version__,
      author='hellman',
      author_email='hellman1908@gmail.com',
      license='MIT',

      url='https://github.com/hellman/libnum',
      description='Some number theoretic functions.',
      long_description=libnum.__doc__,

      packages=['libnum', 'libnum.chains'],
      provides=['libnum'],

      keywords='number prime gcd lcm modular invmod elliptic',
      classifiers=['Development Status :: 2 - Pre-Alpha',
                   'Intended Audience :: Science/Research',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2',
                   'License :: OSI Approved :: MIT License',
                   'Topic :: Scientific/Engineering :: Mathematics',
                   'Topic :: Security :: Cryptography',
                  ],
     )
