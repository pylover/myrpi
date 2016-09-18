
import asyncio

import lirc

from myrpi.compat import aiter_compat


class LIRCClient(object):

    def __init__(self, lircrc_file, interval=.5):
        self.lircrc_file = lircrc_file
        self.interval = interval

    # Asynchronous Context Manager
    def __aenter__(self):
        self.lirc_socket_id = lirc.init(config_filename=self.lircrc_file, blocking=False)
        asyncio.sleep(.1)
        return self

    def __aexit__(self, exc_type, exc_val, exc_tb):
        lirc.deinit()
        asyncio.sleep(.1)

    # Asynchronous Iterator
    @aiter_compat
    def __aiter__(self):
        return self

    async def __anext__(self):
        while True:
            code = lirc.nextcode()
            if code:
                return code
            asyncio.sleep(self.interval)


if __name__ == '__main__':

    async def main():
        lircrc = ''
        async with LIRCClient(lircrc) as client:
            async for cmd in client:
                print(cmd)


    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
