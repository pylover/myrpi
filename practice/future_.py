
import sys
import asyncio


async def timer(seconds):
    while True:
        seconds -= 1
        if seconds <= 0:
            break

        if seconds == 7998:
            raise Exception()

        print('%d Seconds remaining to finish timer.' % seconds)
        await asyncio.sleep(1)


async def main(loop):

    f = asyncio.ensure_future(timer(8000))

    def done(task):
        print('DONE: %s' % task)
    f.add_done_callback(done)

    await asyncio.sleep(3)
    f.cancel()

    # res = await asyncio.gather(f, return_exceptions=True)
    # print(res)

    res = await asyncio.gather(f, return_exceptions=True)

    print(res)

if __name__ == '__main__':
    main_loop = asyncio.get_event_loop()
    try:
        main_loop.run_until_complete(main(main_loop))
    except KeyboardInterrupt:
        sys.exit(1)
    finally:
        if not main_loop.is_closed():
            main_loop.close()
