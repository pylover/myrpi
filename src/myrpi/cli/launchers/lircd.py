
import asyncio

from aiolirc import IRCDispatcher, LIRCClient

from myrpi.cli.launchers.base import ConfiguredLauncher
from myrpi.configuration import settings


class LIRCdLauncher(ConfiguredLauncher):

    @classmethod
    def create_parser(cls, subparsers):
        parser = subparsers.add_parser('lircd', help="Infra-red command dispatcher daemon.")
        return parser

    async def _launch(self):
        from myrpi.car_audio import RPIGPIOContext

        async with RPIGPIOContext(), LIRCClient(
                settings.lirc.lircrc_prog, lircrc_file=settings.lirc.lircrc_file,
                check_interval=settings.lirc.check_interval) as client:
            dispatcher = IRCDispatcher(client)
            result = (await asyncio.gather(dispatcher.listen(), return_exceptions=True))[0]
            print('###############', result)

        if isinstance(result, Exception):
            raise result
    
    def launch(self):
        main_loop = asyncio.get_event_loop()
        try:
            main_loop.run_until_complete(self._launch())
        except KeyboardInterrupt:
            print('__NAME__ CTRL+C pressed.')
            return 1
        finally:
            if not main_loop.is_closed():
                main_loop.close()
