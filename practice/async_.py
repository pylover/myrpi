import asyncio
import sys

from aiolirc import Dispatcher


@Dispatcher.listen_for('amp power', repeat=10)
async def amp_power(loop):
    print("############### AMP POWER #############")


@Dispatcher.listen_for('amp power', repeat=2)
async def amp_source(loop):
    print("APM SOURCE")


async def main(loop):
    dispatcher = Dispatcher('../src/myrpi/conf/lircrc', 'CAR_AMP', max_stack_size=30)
    await dispatcher.capture()
#    async with dispatcher:
#        while True:
#            print(await dispatcher._next_raw())
#        async for i in dispatcher:
#            print(i)
    

if __name__ == '__main__':
    try:
       
            

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(loop))
    except KeyboardInterrupt:
        sys.exit(1)


