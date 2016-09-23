import re
import os
from setuptools import setup, find_packages, Extension

from Cython.Build import cythonize


with open(os.path.join(os.path.dirname(__file__), 'myext.pyx')) as v_file:
    package_version = re.compile(r".*__version__ = '(.*?)'", re.S).match(v_file.read()).group(1)


dependencies = [
    'cython',
]


extensions = [
    Extension('myext', ['myext.pyx'])
]


setup(
    name='myext',
    version=package_version,
    install_requires=dependencies,
    packages=find_packages(),
    ext_modules=cythonize(extensions),
    classifiers=[
        'Programming Language :: Python :: 3.5'
    ]
)
