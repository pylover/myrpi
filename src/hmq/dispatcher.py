# -*- coding: utf-8 -*-
from hmq.listener import Listener
from hmq.message import Message

__author__ = 'vahid'


class Dispatcher(object):

    async def dispatch(self, message: Message):
        raise NotImplementedError

    def register(self, listener: Listener):
        raise NotImplementedError
