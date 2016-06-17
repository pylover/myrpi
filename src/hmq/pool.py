import asyncio
from hmq.configuration import settings
from hmq.dispatcher import Dispatcher
from hmq.worker import Worker


class WorkerPool(object):
    message_queue = None

    def __init__(self, dispatcher: Dispatcher):
        self.dispatcher = dispatcher
        self.message_queue = asyncio.Queue(maxsize=settings.queue.maxsize)
        self.workers = list(self.create_workers())

    def create_workers(self):
        for i in range(settings.workers.count):
            yield Worker(self.message_queue, self.dispatcher)

    def stop(self):
        for w in self.workers:
            w.stop = True

    async def run(self):
        await asyncio.gather(*[w.run() for w in self.workers])
