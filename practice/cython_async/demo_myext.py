
import asyncio

from myext import MyClass

async def main():
    async with MyClass() as c:
        async for i in c:
            print(i)

        print(c.exists('~/.config'))


if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print('CTRL+C Pressed.')
    finally:
        if not loop.is_closed():
            loop.close()
