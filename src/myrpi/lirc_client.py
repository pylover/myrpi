
import asyncio
from os.path import join, abspath, dirname

import lirc

from myrpi.compat import aiter_compat


class LIRCClient(object):
    _last_code = None
    _cancel_capture_flag = None

    def __init__(self, lircrc_prog, lircrc_file, check_interval=.02, capture_interval=.2):
        self.lircrc_prog = lircrc_prog
        self.lircrc_file = lircrc_file
        self.check_interval = check_interval
        self.capture_interval = capture_interval

    # Asynchronous Context Manager
    async def __aenter__(self):
        self.lirc_socket_id = lirc.init(self.lircrc_prog, config_filename=self.lircrc_file, blocking=False)
        await asyncio.sleep(.1)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print('Cleanup')
        lirc.deinit()

    # Asynchronous Iterator

    def next(self):
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
            captured_code = self.next()
            if not captured_code: 
                await asyncio.sleep(self.capture_interval)

        repetition = 1
        cancel_handle = loop.call_later(self.capture_interval, self.cancel_capture)
        try:
            while not self._cancel_capture_flag:
                code = self.next()
                if not code:
                    await asyncio.sleep(self.check_interval)

                elif captured_code != code:
                    print('captured_code != code, %s != %s' % (captured_code, code))
                    cancel_handle.cancel()
                    self._last_code = code
                    break

                else:
                    repetition += 1

            return captured_code, repetition

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
    lircrc_file = join(this_dir, 'conf', 'lircrc')
    print("Using lircrc file: %s" % lircrc_file)

    async def main():
        async with LIRCClient('CAR_AMP', lircrc_file) as client:
            async for cmd in client:
                print(cmd)

    try:

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print('CTRL+C detected !')

