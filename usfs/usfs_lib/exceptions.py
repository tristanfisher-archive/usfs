class USFSException(Exception):
    def __init__(self, message):
        self.message = message

class USFSNetException(USFSException):
    def __init__(self, message):
        self.message = message