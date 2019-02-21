import logging
import datetime


# create logger
class Logger:
    logger = None

    def __init__(self):
        self.logger = logging.getLogger("Enzo_MIDI_IO_Logger:  {}".format(datetime.datetime.now()))
        self.logger.info("Create Initial Instance")

    def get_logger(self):
        return self.logger

    def write_log(self, message):
        self.logger.info("{}: {}".format(datetime.datetime.now(), message))


# Parent base class to handle bespoke errors
class ErrorHandler(Exception):
    logs = None

    def __init__(self):
        self.logs = Logger()

    def get_logs(self):
        return self.logs

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

        super().get_logs().write_log("\n Exp: {}\n Msg: {}".format(expression, message))


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
