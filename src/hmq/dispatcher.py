# -*- coding: utf-8 -*-
from hmq.listener import Listener
from hmq.message import Message
from pymlconf import ConfigManager

__author__ = 'vahid'


class Dispatcher(object):
    default_config = """
    """

    def __init__(self, config=None):
        self.config = ConfigManager(init_value=self.default_config)
        self.listeners = {}
        if config is not None:
            self.configure(config)

    async def dispatch(self, message: Message):
        rule = self.rules.get(message.type_)
        listener_names = rule.listeners
        for listener_name in listener_names:
            listener = self.listeners[listener_name]
            await listener.receive(message)

    def register(self, listener: Listener):
        self.listeners[listener.name] = listener

    def configure(self, config):
        self.config.merge(config)

    @property
    def rules(self):
        return self.config['rules']
