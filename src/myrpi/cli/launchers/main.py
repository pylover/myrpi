
import sys
import argparse

import argcomplete

from myrpi.cli.launchers.base import Launcher
from myrpi.cli.launchers.version import VersionLauncher
from myrpi.cli.launchers.lircd import LIRCdLauncher


# noinspection PyAbstractClass
class MainLauncher(Launcher):

    def __init__(self):
        self.parser = parser = argparse.ArgumentParser(description='MyRPI')
        parser.add_argument('-c', '--config-file', metavar="FILE",
                            help='List of configuration files separated by space. Default: ""')
        parser.add_argument('-d', '--config-dir', metavar="DIR",
                            help='List of configuration directories separated by space. Default: ""')
        parser.add_argument('-v', '--version', action='store_true', default=False, help='Print the version.')

        subparsers = parser.add_subparsers(title="sub commands", prog='hazelnut', dest="command")

        VersionLauncher.register(subparsers)
        LIRCdLauncher.register(subparsers)

        argcomplete.autocomplete(parser)

    def launch(self, args=None):

        if args:
            cli_args = self.parser.parse_args(args)
        else:
            cli_args = self.parser.parse_args()

        if cli_args.version:
            VersionLauncher()()
            return

        if not hasattr(cli_args, 'func'):
            self.parser.print_help()
            return

        sys.exit(cli_args.func(cli_args))

