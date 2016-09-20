
import asyncio
import time

cancel_flag = False

async def main(loop):
    global cancel_flag

    def cancel():
        global cancel_flag
        print("Canceling.")
        cancel_flag = True

    loop.call_later(.5, cancel)

    starttime = loop.time()
    while not cancel_flag:
        print(time.time())
        await asyncio.sleep(.001)
    endtime = loop.time()
    print("Taken: %s" % (endtime - starttime))


if __name__ == '__main__':
    main_loop = asyncio.get_event_loop()
    main_loop.run_until_complete(main(main_loop))
