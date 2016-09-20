
import asyncio
from os.path import join, abspath, dirname

import lirc

from myrpi.compat import aiter_compat


class LIRCClient(object):
    _last_code = None

    def __init__(self, lircrc_prog, lircrc_file, check_interval=.01, capture_interval=.1):
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

    async def capture(self):
        cancel_flag = False

        def cancel():
            nonlocal cancel_flag
            cancel_flag = True

        cancel_handle = loop.call_later(self.capture_interval, cancel)

        if self._last_code is not None:
            captured_code = self._last_code
            repetition = 1
        else:
            captured_code = None
            repetition = 0

        while not cancel_flag:
            code = lirc.nextcode()
            if not code:
                asyncio.sleep(self.check_interval)

            elif captured_code is None:
                captured_code = code
                repetition += 1

            elif captured_code != code:
                cancel_handle.cancel()
                self._last_code = code
                break

            else:
                repetition += 1

        return captured_code, repetition

    @aiter_compat
    def __aiter__(self):
        return self

    async def __anext__(self):
        while True:
            return self.capture()


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

