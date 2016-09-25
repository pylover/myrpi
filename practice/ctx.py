
import asyncio
import sys


class Context(object):

    def __init__(self, name):
        self.name = name

    async def __aenter__(self):
        print('%s: __aenter__' % self.name)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print('%s: __aexit__' % self.name)

async def worker():
    print('working')
    while True:
        await asyncio.sleep(2)


async def main(loop):
    async with Context('CTX1'), Context('CTX2'):
        await worker()


if __name__ == '__main__':
    main_loop = asyncio.get_event_loop()
    try:
        sys.exit(main_loop.run_until_complete(main(main_loop)))
    except KeyboardInterrupt:
        print('__NAME__ CTRL+C pressed.')
        sys.exit(1)
    finally:
        if not main_loop.is_closed():
            main_loop.close()
