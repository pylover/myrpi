# -*- coding: utf-8 -*-
import cyaio_demo
import pyaio_demo
import sys
import asyncio
from datetime import datetime
__author__ = 'vahid'

WORKERS = 10
ITERATIONS = 600


async def runner(f):
    start_time = datetime.now()
    await asyncio.wait([f(i, ITERATIONS) for i in range(WORKERS)])
    return (datetime.now() - start_time).total_seconds()


async def benchmark():
    cython = await runner(cyaio_demo.worker)
    print('Cython: %.5Fs' % cython)
    python = await runner(pyaio_demo.worker)
    print('CPython: %.5Fs' % python)
    print('Cython is %dX faster than CPython' % round(python / cython))


def main():
    loop = asyncio.get_event_loop()
    ret = loop.run_until_complete(benchmark())
    loop.close()
    return ret


if __name__ == '__main__':
    sys.exit(main())


