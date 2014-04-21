#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
from distutils.core import setup

import libnum


setup(name='libnum',
      version='1.4',
      author='hellman',
      author_email='hellman1908@gmail.com',
      url='https://github.com/hellman/libnum',
      download_url='https://github.com/hellman/libnum',
      description='Some number theoretic functions.',
      long_description=libnum.__doc__,
      packages=['libnum'],
      provides=['libnum'],
      keywords='number prime gcd lcm invmod elliptic',
      license='MIT License',
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
