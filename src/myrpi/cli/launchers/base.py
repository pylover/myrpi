
import asyncio


class Launcher(object):
    parser = None
    no_launch = False

    @classmethod
    def create_parser(cls, subparsers):
        raise NotImplementedError

    @classmethod
    def register(cls, subparsers):
        parser = cls.create_parser(subparsers)
        instance = cls()
        instance.parser = parser
        if not cls.no_launch:
            parser.set_defaults(func=instance)
        return instance

    def __call__(self, *args):
        if len(args):
            self.args = args[0]
        else:
            self.args = None

        if asyncio.iscoroutinefunction(self.launch):
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(self.launch())
        else:
            return self.launch()

    def launch(self):
        if self.parser is None:
            raise ValueError('Invalid parser')
        self.parser.print_help()


# noinspection PyAbstractClass
class ConfiguredLauncher(Launcher):

    def configure(self, args):
        from myrpi.configuration import init
        init(directories=args.config_dir, files=args.config_file)

    def __call__(self, *args):
        self.configure(args[0])
        return super().__call__(*args)


class RequireSubCommand(object):
    no_launch = True
