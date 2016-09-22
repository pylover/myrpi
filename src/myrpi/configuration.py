
from os.path import exists, join

from pymlconf import ConfigManager
from appdirs import user_config_dir

from myrpi.proxy import ObjectProxy

_settings = None
settings = ObjectProxy(lambda: _settings)


__builtin_config = """

lirc:
  lircrc_file: $(user_config_dir)s/lircrc
  lircrc_prog: MyRPI
  max_stack_size: 30
  check_interval: .1
  empty_skip: 5

"""


class Configurable(object):
    def __init__(self, **kwargs):

        if hasattr(self, '__config_key__'):
            config_key = getattr(self, '__config_key__')
        else:
            config_key = self.__class__.__name__

        config = settings.get(config_key)
        if config is None:
            raise ConfigurationException('Config key %s not found.' % config_key)

        config.merge(kwargs)

        for k, v in config.items():
            setattr(self, k, v)


class ConfigurationException(Exception):
    pass


class ConfigurationAlreadyInitializedException(Exception):
    pass


def init(config=None, directories=None, files=None, force=False):
    """
    Initialize the configuration manager
    :param config: `string` or `dict`
    :param directories: semi-colon separated `string` or `list` of director(y|es)
    :param files: semi-colon separated `string` or `list` of file(s)
    :param force: force initialization even if it's already initialized
   """
    global _settings

    if not force and _settings is not None:
        raise ConfigurationAlreadyInitializedException("Configuration manager object is already initialized.")

    context = {
        'user_config_dir': user_config_dir()
    }

    _settings = ConfigManager(__builtin_config, context=context)

    if config:
        _settings.merge(config)

    local_config_file = join(user_config_dir(), 'myrpi.yaml')
    if exists(local_config_file):
        print('Loading config file: %s' % local_config_file)
        _settings.load_files(local_config_file)

    if directories:
        _settings.load_dirs(directories)

    if files:
        _settings.load_files(files)

    return _settings


