# -*- coding: utf-8 -*-
__author__ = 'vahid'


async def worker(int worker_idx, int iterations):
    cdef int i, result, o = iterations * worker_idx
    for i in range(o):
        result += i**i
    for i in range(o):
        result -= i**i
    return result

