import logging
import sensorPiClass


# Parent class to handle bespoke errors
class ErrorHandler(Exception):
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


class IRConnectionError(ErrorHandler):
    pass


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

    @staticmethod
    def led_feedback():
        # Flash the red (FAIL) LED
        print("Connection to broker unsuccessful")
        spi.flash_led(spi.FAIL_LED, 2)


class MIDIConnectionError(ErrorHandler):
    pass


class MutexError(ErrorHandler):
    pass


class UndefinedSateError(ErrorHandler):
    pass
