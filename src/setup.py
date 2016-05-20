# -*- coding: utf-8 -*-
from distutils.core import setup
from Cython.Build import cythonize

__author__ = 'vahid'


setup(
    name='HMQ',
    ext_modules=cythonize("hello.pyx"),
)
