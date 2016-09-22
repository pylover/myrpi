
import myrpi
from myrpi.cli.launchers.base import Launcher


class VersionLauncher(Launcher):
    @classmethod
    def create_parser(cls, subparsers):
        return subparsers.add_parser('version', help='Print the version.')

    def launch(self):
        print(myrpi.__version__)
