import logging


# Parent class to handle bespoke errors
class ErrorHandler(Exception):
    pass


# Child classes for bespoke errors
class AccelConnection(ErrorHandler):
    def __init__(self, expression, message):

        if expression == None:
            self.expression = ""
        else:
            self.expression = expression

        if message == None:
            self.message = "could not establish connection with GyroScope, please check wiring"
        else:
            self.message = message


class IRConnection(ErrorHandler):
    pass


class IRIOError(ErrorHandler):
    pass


class BrokerConnection(ErrorHandler):
    pass


class MIDIConnection(ErrorHandler):
    pass


class MutexError(ErrorHandler):
    pass


class UndefinedSate(ErrorHandler):
    pass
