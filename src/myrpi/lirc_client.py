
import asyncio
from os.path import join, abspath, dirname


from myrpi.compat import aiter_compat


class LIRCClient(object):

    def __init__(self, lircrc_prog, lircrc_file, interval=.5):
        self.lircrc_prog = lircrc_prog
        self.lircrc_file = lircrc_file
        self.interval = interval

    # Asynchronous Context Manager
    async def __aenter__(self):
        self.lirc_socket_id = lirc.init(self.lircrc_prog, config_filename=self.lircrc_file, blocking=False)
        await asyncio.sleep(.1)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        lirc.deinit()
        await asyncio.sleep(.1)

    # Asynchronous Iterator
    @aiter_compat
    def __aiter__(self):
        return self

    async def __anext__(self):
        while True:
            code = lirc.nextcode()
            if code:
                return code
            await asyncio.sleep(self.interval)


if __name__ == '__main__':
    this_dir = abspath(dirname(__file__))
    lircrc_file = join(this_dir, 'conf', 'lircrc')

    async def main():

        async with LIRCClient('irexec', lircrc_file) as client:
            async for cmd in client:
                print(cmd)


    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
