
from cpython.exc cimport PyErr_WarnEx

import os
from aiolirc.compat import aiter_compat


__version__ = '0.1.0'


cdef class Size:
    cdef int width, height

    def __init__(self, w, h):
        self.width = w
        self.height = h

    cdef format(Size self):
        return '<Size w=%s h=%s>' % (self.width, self.height)


cdef class MyClass:
    cdef int counter
    cdef Size size

    def __init__(self):
        PyErr_WarnEx(UserWarning, "My Custom warning", 1)
        self.counter = 0
        self.size = Size(10, 20)
        print(self.size.format())

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
