from hmq.message import Message


class Listener(object):

    def receive(self, message: Message):
        raise NotImplementedError
