
from aiolirc import Dispatcher

from myrpi.cli.launchers.base import ConfiguredLauncher
from myrpi.configuration import settings


class LIRCdLauncher(ConfiguredLauncher):

    @classmethod
    def create_parser(cls, subparsers):
        parser = subparsers.add_parser('ircd', help="Infra-red command dispatcher daemon.")
        return parser

    async def launch(self):

        dispatcher = Dispatcher(
            settings.lirc.lircrc_file,
            settings.lirc.lircrc_prog,
            max_stack_size=settings.lirc.max_stack_size,
            check_interval=settings.lirc.check_interval,
            empty_skip=settings.lirc.empty_skip
        )

        return await dispatcher.capture()
