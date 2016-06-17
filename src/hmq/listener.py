import asyncio
import collections

from hmq.message import Message


class Listener(object):

    def __init__(self, name, bind=None):
        self.name = name
        self._binds = set()
        if bind is not None:
            if not isinstance(bind, collections.Iterable):
                bind = [bind]
            for f in bind:
                self.bind(f)

    async def receive(self, message: Message):
        for f in self._binds:
            if asyncio.iscoroutinefunction(f):
                await f(message)
            else:
                f(message)

    def bind(self, func):
        self._binds.add(func)
        return func

    def unbind(self, func):
        self._binds.remove(func)
        return func


