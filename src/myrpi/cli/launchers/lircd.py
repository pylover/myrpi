
from aiolirc import IRCDispatcher, LIRCClient

from myrpi.cli.launchers.base import ConfiguredLauncher
from myrpi.configuration import settings


class LIRCdLauncher(ConfiguredLauncher):

    @classmethod
    def create_parser(cls, subparsers):
        parser = subparsers.add_parser('ircd', help="Infra-red command dispatcher daemon.")
        return parser

    async def launch(self):
        from myrpi.car_audio import RPIGPIOContext

        async with LIRCClient(
                settings.lirc.lircrc_prog, lircrc_file=settings.lirc.lircrc_file,
                check_interval=settings.lirc.check_interval) as client, \
                RPIGPIOContext():
            try:
                dispatcher = IRCDispatcher(client)
                await dispatcher.listen()
            except KeyboardInterrupt:
                print('CTRL+C is pressed.')
                return 1
