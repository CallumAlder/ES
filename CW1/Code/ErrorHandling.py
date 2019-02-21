
# Parent class to handle bespoke errors
class ErrorHandler(Exception):
    pass

# Child classes for bespoke errors
class AccelConnection(ErrorHandler):
    pass

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