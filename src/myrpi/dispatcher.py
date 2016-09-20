
import asyncio
from random import randint
from os.path import join, abspath, dirname

import lirc

from myrpi.compat import aiter_compat
from myrpi.configuration import Configurable, init as init_config


class LIRCClient(Configurable, asyncio.Lock):
    _last_code = None
    _cancel_capture_flag = None
    emulate = None
    lircrc_prog = None
    lircrc_file = None
    capture_interval = .3
    check_interval = .01

    def __init__(self, *, loop=None, **kwargs):
        Configurable.__init__(self, **kwargs)
        asyncio.Lock.__init__(self, loop=loop)

    # Asynchronous Context Manager
    async def __aenter__(self):
        if self.emulate:
            async def _next():
                await asyncio.sleep(randint(10, 1000) / 1000)
                return [['amp', 'power'], ['amp', 'source'], ['amp', 'play'], []][randint(0, 2)]
            self.next = _next
        else:
            self.lirc_socket_id = lirc.init(self.lircrc_prog, config_filename=self.lircrc_file, blocking=False)
            await asyncio.sleep(.1)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print('Cleanup')
        if not self.emulate:
            lirc.deinit()

    # Asynchronous Iterator
    @staticmethod
    async def _next_raw():
        code = lirc.nextcode()
        if code:
            return code
        return None

    def cancel_capture(self):
        self._cancel_capture_flag = True

    async def capture(self):

        captured_code = None

        if self._last_code is not None:
            captured_code = self._last_code

        while captured_code is None:
            captured_code = await self.next()
            if not captured_code:
                await asyncio.sleep(self.capture_interval)

        repetition = 1
        cancel_handle = self._loop.call_later(self.capture_interval, self.cancel_capture)
        try:
            while not self._cancel_capture_flag:
                code = await self.next()

                if captured_code != code:
                    cancel_handle.cancel()
                    if code:
                        self._last_code = code
                    break

                repetition += 1
                await asyncio.sleep(self.check_interval)

            return tuple(captured_code), repetition

        finally:
            self._cancel_capture_flag = False

    @aiter_compat
    def __aiter__(self):
        return self

    async def __anext__(self):
        while True:
            return await self.capture()


if __name__ == '__main__':
    this_dir = abspath(dirname(__file__))
    lircrc_config_file = join(this_dir, 'conf', 'lircrc')
    print("Using lircrc file: %s" % lircrc_config_file)

    async def main():
        async with LIRCClient(lircrc_prog='CAR_AMP', lircrc_file=lircrc_config_file) as client:
            async for cmd in client:
                print(cmd)

    try:
        init_config()
        main_loop = asyncio.get_event_loop()
        main_loop.run_until_complete(main())
    except KeyboardInterrupt:
        print('CTRL+C detected !')
