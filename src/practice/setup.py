# -*- coding: utf-8 -*-
from distutils.core import setup
from Cython.Build import cythonize

__author__ = 'vahid'


setup(
    name='cyaio',
    ext_modules=cythonize("cyaio_demo.pyx"),
)
