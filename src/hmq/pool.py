from asyncio import Queue
from hmq.configuration import settings


class WorkerPool(object):
    message_queue = None

    def __init__(self):
        self.message_queue = Queue(maxsize=settings.pool.maxsize)

    async def run(self):
        raise NotImplementedError
