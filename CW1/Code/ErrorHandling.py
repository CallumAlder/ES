
# Parent class to handle bespoke errors
class ErrorHandler(Exception):
    pass

# Child classes for bespoke errors
class AccelConnection(ErrorHandler):
    pass

class IRConnection(ErrorHandler):
    pass

class IRIOError(ErrorHandler):
    def __init__(self):
        self.pi = 1

    def reset_IR_sensor(self, ir_sensor):
        print("Error - IR value received =", str(val_ir))
        ir_sensor._reset()
        time.sleep(0.01)
        ir_sensor._load_calibration()
        time.sleep(0.01)
        print("Light Sensor reset")
    pass

class BrokerConnection(ErrorHandler):
    pass

class MIDIConnection(ErrorHandler):
    pass

class MutexError(ErrorHandler):
    pass