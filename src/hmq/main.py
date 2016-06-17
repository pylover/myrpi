import asyncio
from hmq.pool import WorkerPool


def main():
    loop = asyncio.get_event_loop()
    pool = WorkerPool()
    loop.run_until_complete(pool.run())

