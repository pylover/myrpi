# -*- coding: utf-8 -*-
__author__ = 'vahid'


async def worker(worker_idx, iterations):
    result, o = 0, iterations * worker_idx
    for i in range(o):
        result += i**i
    for i in range(o):
        result -= i**i
