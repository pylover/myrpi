import asyncio

from hmq.dispatcher import Dispatcher
from hmq.configuration import settings


class Worker(object):
    def __init__(self, queue: asyncio, dispatcher: Dispatcher):
        self.queue = queue
        self.dispatcher = dispatcher
        self.stop = False

    async def run(self):

        while True:

            try:
                # Wait for new message
                message = await self.queue.get_nowait()

                # Dispatch the message
                await self.dispatcher.dispatch(message)

            except asyncio.QueueEmpty:
                asyncio.sleep(settings.workers.wait)

            # Checking for stop flag
            if self.stop:
                break
