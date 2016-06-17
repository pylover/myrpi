from typing import TypeVar

from hmq.listener import Listener
from hmq.message import Message
from pymlconf import ConfigManager


ConfigData = TypeVar('ConfigData', str, dict)
ConfigFiles = TypeVar('ConfigData', str, list)


class Dispatcher(object):
    default_config = """
    """

    def __init__(self, config: ConfigData=None, config_files: ConfigFiles=None):
        self.config = ConfigManager(init_value=self.default_config)
        self.listeners = {}
        if config is not None:
            self.config.merge(config)
        if config_files:
            self.config.load_files(config_files)

    async def dispatch(self, message: Message):
        rule = self.rules.get(message.type_)
        listener_names = rule.listeners
        for listener_name in listener_names:
            listener = self.listeners[listener_name]
            await listener.receive(message)

    def register(self, listener: Listener):
        self.listeners[listener.name] = listener

    @property
    def rules(self):
        return self.config['rules']
