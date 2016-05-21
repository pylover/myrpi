# -*- coding: utf-8 -*-
__author__ = 'vahid'


cdef void c_worker(int worker_idx, int iterations):
    cdef int i, result, o = iterations * worker_idx
    for i in range(o):
        result += i**i
    for i in range(o):
        result -= i**i


async def worker(int worker_idx, int iterations):
    c_worker(worker_idx, iterations)

