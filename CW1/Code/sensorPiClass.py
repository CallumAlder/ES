import si1145
import time
import pigpio

import numpy as np

from lis3dh import AccGyro
from math import log


class SenPi(object):
    # Class object interfaces the sensors and the raspberry Pi
    def __init__(self, debug=True):
        self.isDebug = debug
        self.debug("Initialising sensor Pi interface object")

        self._GPIO = pigpio.pi()

        # LEDs are used as feedback for: system errors, state changes and successful connections
        self.SUCCESS_LED = 20  # Success LED - Blinks when the guitar module connects to the web broker
        self.FAIL_LED = 16  # Fail LED - Blinks once when a connection error occurs
        self.CHANGE_LED = 26  # Change LED - Blinks when the mapping of sensor data to outputs has changed

        self.init_gpio(self.SUCCESS_LED, 1)
        self.init_gpio(self.CHANGE_LED, 1)
        self.init_gpio(self.FAIL_LED, 1)

        self.test_leds(self.SUCCESS_LED, self.CHANGE_LED, self.FAIL_LED)

        time.sleep(0.1)
        self.lightSensor = si1145.SI1145()
        time.sleep(0.5)
        self.agSensor = AccGyro(debug=True)
        self.agSensor.setRange(AccGyro.RANGE_2G)
        time.sleep(0.25)

        # Weights used for exponential filtering in sensor acquisition
        self.ir_weight = 0.72
        self.x_weight = 0.2
        self.y_weight = 0.3
        self.z_weight = 0.26

        # Topics to listen or publish to
        self.publish_topic1 = "IC.embedded/skadoosh/sensor"
        self.listen_topic1 = "IC.embedded/skadoosh/midi"

    # Initialise GPIO mode of LED pins
    def init_gpio(self, pin, mode):
        if mode == 1:
            self._GPIO.set_mode(pin, pigpio.OUTPUT)
            # TODO: Add an INPUT mode?

    # Test that the LEDs are working by having them all turn on very quickly
    def test_leds(self, success_led, fail_led, chg_led):
        print("Testing LEDS...")
        self._GPIO.write(success_led, 1)
        self._GPIO.write(fail_led, 1)
        self._GPIO.write(chg_led, 1)

        time.sleep(2)

        self._GPIO.write(success_led, 0)
        self._GPIO.write(fail_led, 0)
        self._GPIO.write(chg_led, 0)

    # Make the LEDs flash for some duration of time
    def flash_led(self, led, duration):
        self._GPIO.write(led, 1)
        time.sleep(duration)
        self._GPIO.write(led, 0)

    def sensor_calibration(self):
        print("Extracting calibration parameters")
        # Number of calibration trials
        cal_trials = 100

        max_ir = 0
        min_ir = 1000000

        max_x = 0
        min_x = 1000000

        max_y = 0
        min_y = 1000000

        max_z = 0
        min_z = 1000000

        n = 0
        while n < cal_trials:
            # IR sensor calibration (for proximity sensing) tuned on a log scale
            cal_ir = 0
            try:
                cal_ir = log(self.lightSensor.readIR())
            except ValueError:
                print("Error - IR value received =", str(cal_ir))
                n -= 1
                continue

            max_ir, min_ir = self.min_max_test(raw=cal_ir, max=max_ir, min=min_ir, med_bool=None)

            # Gyroscope data calibration (to get a sense of left versus right)
            max_x, min_x = self.min_max_test(raw=self.agSensor.getX(), max=max_x, min=min_x, med_bool=None)
            max_y, min_y = self.min_max_test(raw=self.agSensor.getY(), max=max_y, min=min_y, med_bool=None)
            max_z, min_z = self.min_max_test(raw=self.agSensor.getZ(), max=max_z, min=min_z, med_bool=None)

            n += 1
            time.sleep(0.01)

        # Get calibration arrays
        cal_max_array = np.array([max_ir, max_x, max_y, max_z])
        print("Max array:", cal_max_array)

        cal_min_array = np.array([min_ir, min_x, min_y, min_z])
        print("Min array:", cal_min_array)

        cal_med_array = np.add(cal_max_array, cal_min_array) / 2
        print("Median array:", cal_med_array)

        return cal_max_array, cal_min_array, cal_med_array

    # Static method => does not rely on attributes of the object, it is used to get min and max values
    @staticmethod
    def min_max_test(raw, max, min, med_bool):
        if raw >= max:
            if med_bool is None:
                return raw, min
            return raw, min, True
        elif raw < max:
            if min < 0 and abs(raw) > abs(min):
                if med_bool is None:
                    return max, raw
                return max, raw, True
            elif min > 0 and raw < min:
                if med_bool is None:
                    return max, raw
                return max, raw, True

        # If it reaches this point, it is because no values have changed
        if med_bool is None:
            return max, min
        return max, min, False

    # The method is used to determine what data values to send to the MQTT broker
    @staticmethod
    def to_send(curr_ir, curr_x, curr_y, curr_z):
        if (curr_ir + curr_x + curr_y + curr_z) == -4:
            return "nan"
        else:
            return str(curr_ir) + "," + str(curr_x) + "," + str(curr_y) + "," + str(curr_z)

    @staticmethod
    def update_sensor_out(curr, val, max_val, med_val, min_val, weight, threshold):
        scaled_val = ((val - med_val) / (max_val - min_val)) + 0.5
        scaled_val = ((1 - weight) * curr) + (weight * 128 * scaled_val)
        if abs(curr - scaled_val) >= threshold:
            curr = scaled_val
            print_val = int(curr)
        else:
            print_val = -1
        return curr, print_val

    def debug(self, msg):
        if not self.isDebug:
            return
        print(msg)
