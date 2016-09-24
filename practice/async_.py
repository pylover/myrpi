import asyncio
import sys

from aiolirc import quickstart, listen_for


@listen_for('amp power', repeat=10)
async def amp_power(loop):
    print("############### AMP POWER #############")


@listen_for('amp source', repeat=2)
async def amp_source(loop):
    print("APM SOURCE")


@listen_for('off', repeat=2)
async def amp_source(loop):
    print("OFF")


async def main(loop):
    await quickstart(lircrc_prog='MyRPI')


if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(loop))
    except KeyboardInterrupt:
        sys.exit(1)


