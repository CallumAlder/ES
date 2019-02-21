import sensorPiClass
import logging
import datetime
import time


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
class AccelConnectionError(ErrorHandler):
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


class IRConnectionError(ErrorHandler):
    def __init__(self, expression, message):

        if expression == None:
            self.expression = ""
        else:
            self.expression = expression

        if message == None:
            self.message = "could not establish connection with IR device, please serial port connections"
        else:
            self.message = message

        super().get_logs().write_log("\n Exp: {}\n Msg: {}".format(expression, message))



class IRIOError(ErrorHandler):
    def __init__(self, expression, message, ir_sensor):

        if expression == None:
            self.expression = ""
        else:
            self.expression = expression

        if message == None:
            self.message = "IR sensor requires resetting"
        else:
            self.message = message

        self.ir_sensor = ir_sensor
        self.reset_ir_sensor(self.ir_sensor)

        super().get_logs().write_log("\n Exp: {}\n Msg: {}\n IR: {}".format(expression, message,ir_sensor))

    @staticmethod
    def reset_ir_sensor(ir_sensor):
        ir_sensor._reset()
        time.sleep(0.01)

        ir_sensor._load_calibration()
        time.sleep(0.01)
        print("Light Sensor reset")


class BrokerConnectionError(ErrorHandler):
    def __init__(self, expression, message):

        if expression == None:
            self.expression = ""
        else:
            self.expression = expression

        if message == None:
            self.message = "could not establish connection with MQTT Broker, try reconnecting web app"
        else:
            self.message = message

        self.led_feedback()
        self.spi = sensorPiClass.SenPi()

        super().get_logs().write_log("\n Exp: {}\n Msg: {}".format(expression, message))

    def led_feedback(self):
        # Flash the red (FAIL) LED
        print("Connection to broker unsuccessful")
        self.spi.flash_led(spi.FAIL_LED, 2)


class MIDIConnectionError(ErrorHandler):
    def __init__(self, expression, message):

        if expression == None:
            self.expression = ""
        else:
            self.expression = expression

        if message == None:
            self.message = "could not establish connection with MIDI device, please check serial port connections"
        else:
            self.message = message

        super().get_logs().write_log("\n Exp: {}\n Msg: {}".format(expression, message))



class MutexError(ErrorHandler):
    pass


class UndefinedSateError(ErrorHandler):
    pass
