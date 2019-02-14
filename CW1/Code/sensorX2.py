import si1145
# import bluetooth
import time
import datetime
import json
import paho.mqtt.client as mqtt
import pigpio

import numpy as np

from lis3dh import AccGyro
from time import sleep
from math import log

GPIO = pigpio.pi()

SUCCESS_LED = 20    # Success LED
GPIO.set_mode(SUCCESS_LED, pigpio.OUTPUT)

FAIL_LED = 16
GPIO.set_mode(FAIL_LED, pigpio.OUTPUT)

print("Testing LEDS...")
GPIO.write(SUCCESS_LED, 1)
GPIO.write(FAIL_LED, 1)
time.sleep(2)
GPIO.write(SUCCESS_LED, 0)
GPIO.write(FAIL_LED, 0)

def on_publish(client, userdata, mid):
   print("mid: "+ str(mid))

def on_message(client, userdata, msg):
   msg = str(msg.payload.decode())
   print("msg: " + msg)

   if msg == "lol@cig":
       print("Turn success LED on...")
       GPIO.write(SUCCESS_LED, 1)
       time.sleep(2)
       GPIO.write(SUCCESS_LED, 0)
   return msg


def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))
    client.subscribe("IC.embedded/skadoosh/midi")

def extract_data(s_data):
    s_data = s_data.replace("b", "")
    s_data = s_data.replace("'", "")
    s_data = s_data.split(",")

    json_data = {"prx": s_data[0], "xGy": s_data[1], "yGy": s_data[2], "zGy": s_data[3]}

    # print("JSON Data:", json_data)
    return json_data

def min_max_test(raw, max, min):
    if raw >= max:
        return raw, min, True
    elif raw < max:
        if min < 0 and abs(raw) > abs(min):
            return max, raw, True
        elif min > 0 and raw < min:
            return max, raw, True
        else:
            return max, min, False
    else:
        return max, min, False

def get_min(min_value):
    if min_value == 0:
        return 0
    else:
        return log(min_value)

def lin_calibration():
    print("Extracting calibration parameters")
    cal_trials = 100
    n = 0

    max_ir = 0
    min_ir = 1000000

    max_x = 0
    min_x = 1000000

    max_y = 0
    min_y = 1000000

    max_z = 0
    min_z = 1000000

    med_array = np.zeros(4)

    while n < cal_trials:
        cal_ir = log(lightSensor.readIR())
        max_ir, min_ir, update_med = min_max_test(cal_ir,
                                                  max_ir,
                                                  min_ir)
        if update_med:
            med_array[0] = (max_ir + min_ir)/2

        # Include gyro data so you can tell which direction is left and which is right
        max_x, min_x, update_med = min_max_test(agSensor.getX(),
                                                max_x,
                                                min_x)
        if update_med:
            med_array[1] = (max_x + min_x)/2

        max_y, min_y, update_med = min_max_test(agSensor.getY(),
                                                max_y,
                                                min_y)
        if update_med:
            med_array[2] = (max_y + min_y)/2

        max_z, min_z, update_med = min_max_test(agSensor.getZ(),
                                                max_z,
                                                min_z)
        if update_med:
            med_array[3] = (max_z + min_z)/2

        # if (n % 25) == 0:
        #     print("Trial count:", n)
        n += 1
        time.sleep(0.01)

    max_array = np.array([max_ir,
                          max_x,
                          max_y,
                          max_z])
    print("Max array:", max_array)

    min_array = np.array([min_ir,
                          min_x,
                          min_y,
                          min_z])
    print("Min array:", min_array)

    med_array = np.add(max_array, min_array) / 2
    print("Median array:", med_array)

    return max_array, min_array, med_array

if __name__ == '__main__':

    ALL_DATA = 1
    LIGHT_DATA = 2
    GYRO_DATA = 3

    # Make a dynamic calibration method
    # Make a thread for updating standard deviation and mean w/o significant overhead
    # Have separate threads for each sensor?

    current_ir = 0
    current_x = 0
    current_y = 0
    current_z = 0

    ir_weight = 0.72
    x_weight = 0.2
    y_weight = 0.3
    z_weight = 0.26

    # Specify topic to subscribe and publish to
    publish_topic1 = "IC.embedded/skadoosh/sensor"
    listen_topic1 = "IC.embedded/skadoosh/midi"

    broker = "iot.eclipse.org"
    port = 1883

    client = mqtt.Client()
    client.on_publish = on_publish
    client.on_message = on_message
    client.on_connect = on_connect

    # X = client.connect(broker, port=port)
    X = -1

    start = time.time()
    while X != 0:
        time.sleep(0.5)
        try:
            X = client.connect(broker, port=port)
        except:
            print("RED LED on")
            GPIO.write(FAIL_LED, 1)
            time.sleep(2)
            GPIO.write(FAIL_LED, 0)
            print(X)

    # Sensor initialisation
    lightSensor = si1145.SI1145()
    agSensor = AccGyro(debug=True)
    agSensor.setRange(AccGyro.RANGE_2G)
    time.sleep(1)

    max_array, min_array, med_array = lin_calibration()
    print("Parameters for calibration extracted.")

    if X == 0:

        client.loop_start()
        while True:
            ir = ir_weight * 1.47 * log(lightSensor.readIR())
            max_array[0], min_array[0], update_med = min_max_test(ir,
                                                                  max_array[0],
                                                                  min_array[0])
            if update_med:
                med_array[0] = (max_array[0] + min_array[0]) / 2
            scaled_ir = ((ir - med_array[0]) / (max_array[0] - min_array[0])) + 0.5
            scaled_ir = (1 - ir_weight) * current_ir + ir_weight * 128 * scaled_ir
            if abs(current_ir - scaled_ir) >= 8:
                current_ir = scaled_ir
                print_ir = int(current_ir)
            else:
                print_ir = -1

            x = agSensor.getX()
            max_array[1], min_array[1], update_med = min_max_test(x,
                                                                  max_array[1],
                                                                  min_array[1])
            if update_med:
                med_array[1] = (max_array[1] + min_array[1]) / 2
            scaled_x = ((x - med_array[1]) / (max_array[1] - min_array[1])) + 0.5
            scaled_x = (1 - x_weight) * current_x + x_weight * 128 * scaled_x
            if abs(current_x - scaled_x) >= 17:
                current_x = scaled_x
                print_x = int(current_x)
            else:
                print_x = -1

            y = agSensor.getY()
            max_array[2], min_array[2], update_med = min_max_test(y,
                                                                  max_array[2],
                                                                  min_array[2])
            if update_med:
                med_array[2] = (max_array[2] + min_array[2]) / 2
            scaled_y = ((y - med_array[2]) / (max_array[2] - min_array[2])) + 0.5
            scaled_y = (1 - y_weight) * current_y + y_weight * 128 * scaled_y
            if abs(current_y - scaled_y) >= 15:
                current_y = scaled_y
                print_y = int(current_y)
            else:
                print_y = -1

            z = agSensor.getZ()
            max_array[3], min_array[3], update_med = min_max_test(z,
                                                                  max_array[3],
                                                                  min_array[3])
            if update_med:
                med_array[3] = (max_array[3] + min_array[3]) / 2
            scaled_z = ((z - med_array[3]) / (max_array[3] - min_array[3])) + 0.5
            scaled_z = (1 - z_weight) * current_z + z_weight * 128 * scaled_z
            if abs(current_z - scaled_z) >= 15:
                current_z = scaled_z
                print_z = int(current_z)
            else:
                print_z = -1

            if print_ir != -1:
                data = str(print_ir)
            else:
                data = str("-1")

            if print_x != -1:
                data += "," + str(print_x)
            else:
                data += ",-1"

            if print_y != -1:
                data += "," + str(print_y)
            else:
                data += ",-1"

            if print_z != -1:
                data += "," + str(print_z)
            else:
                data += ",-1"

            if data != "-1,-1,-1,-1":
                # client_socket.send(data)
                currentTime = datetime.datetime.now()
                print("Message sent at:", currentTime)

                j_data = extract_data(data)
                print("Publishing to " + publish_topic1 + "...")
                print(mqtt.error_string(client.publish(topic=publish_topic1, payload=json.dumps(j_data), qos=1).rc))
                # client.publish(topic=publish_topic1, payload=json.dumps(j_data), qos=1)

            sleep(0.06)
            # client.loop_stop()

    else:
        print("Pas de connexion")

    client.loop_stop()
    client.disconnect()
