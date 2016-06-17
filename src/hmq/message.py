

class Message(object):
    type_ = None

    def __init__(self, type_, data=None):
        self.type_ = type_
        self.data = data

