from hmq.pool import WorkerPool


async def main():
    pool = WorkerPool()
    await pool.run()
