# -*- coding: utf-8 -*-
from setuptools import setup as setuptools_setup, find_packages
from Cython.Build import cythonize

__author__ = 'vahid'


dependencies = [
    'Cython',
    'pymlconf',
    'daemonize',
]


# pycharm inspection fix-up: redirecting `requirements` to `install_requires`
def setup(**kw):
    kw['install_requires'] = kw['requires']
    del kw['requires']
    setuptools_setup(**kw)


setup(
    name='HMQ',
    ext_modules=cythonize("hello.pyx"),
    requires=dependencies,
    packages=find_packages(),
)
