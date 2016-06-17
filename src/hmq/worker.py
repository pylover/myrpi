

class Worker(object):
    def __init__(self, queue):
        self.queue = queue

    async def run(self):
        raise NotImplementedError
