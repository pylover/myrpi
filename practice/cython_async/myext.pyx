
from cpython.exc cimport PyErr_WarnEx

import os
from aiolirc.compat import aiter_compat


__version__ = '0.1.0'


cdef class MyClass:
    cdef int counter

    def __init__(self):
        PyErr_WarnEx(UserWarning, "My Custom warning", 1)
        self.counter = 0

    async def __aenter__(self):
        print('__aenter__')
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print('__aexit__')

    def __aiter__(self):
        return aiter_compat(self)

    def exists(MyClass self not None, filename):
        return os.path.exists(filename)

    async def __anext__(self):
        self.counter += 1
        if self.counter > 10:
            raise StopAsyncIteration
        return self.counter
