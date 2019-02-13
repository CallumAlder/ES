import si1145
import bluetooth
import time
import datetime
import json

import numpy as np


from lis3dh import AccGyro
from time import sleep
from math import log

# Sensor initialisation
lightSensor = si1145.SI1145()

agSensor = AccGyro(debug=True)
agSensor.setRange(AccGyro.RANGE_2G)
# second accelerometer
# s2 = AccGyro(address=0x19, debug=True)

ALL_DATA = 1
LIGHT_DATA = 2
GYRO_DATA = 3

# Bluetooth setup
bd_addr = "B8:27:EB:BF:51:05"

port = 1
client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
client_socket.connect((bd_addr, port))

# test_array = np.empty((0, 5), float)
# test_array = np.append(test_array, [[1.0, 2.0, 5, 71.2, 4.0]], axis=0)
# test_array = np.append(test_array, [[1.0, 3.0, 34.23, 12.1, 4.33]], axis=0)
# print(test_array[0, :])

# mean_test_array = np.mean(test_array, axis=0)
# print(mean_test_array)

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

    # # Arrays contain either: maximum, minimum or median values for sensors at rest
    # Sidenote: It seemed to take offence against this method of approach so abort lol
    # max_array = np.zeros(4)
    # min_array = np.array([100000.0, 100000.0, 100000.0, 100000.0])
    med_array = np.zeros(4)

    # print("Max array (start):", max_array[0])
    # print("Min array (start):", min_array[0])
    # print("Med array (start):", med_array[0])

    while n < cal_trials:
        # cal_ir = lightSensor.readIR()
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

        if (n % 25) == 0:
            print("Trial count:", n)
        n += 1
        time.sleep(0.01)

    # max_array = np.array([max_ir, max_x, max_y, max_z])
    # Gyroscope: Use minimum value as an offset to change range from 0 to gy_max + abs(gy_min)
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

max_array, min_array, med_array = lin_calibration()

# TODO: Normal distribution - see below
# def get_mean(mean, x_n, n):
#     if mean == None:
#         return x_n
#     else:
#         return (mean*(n-1))/n
#
# def get_variance(mean, sqr_sum, n):
#     return (sqr_sum/n)-pow(mean, 2)

# def norm_calibration():
#     print("Extracting calibration parameters")
#     n = 1
#     cal_trials = 250
#     # cal_array = np.empty((0, 6))
#
#     mean_ir = 0
#     sq_ir = 0
#
#     mean_x = 0
#     sq_x = 0
#
#     mean_y = 0
#     sq_y = 0
#
#     mean_z = 0
#     sq_z = 0
#
#     # Turn into a matrix or a series of 1D arrays ples
#     # max_vis = 0
#     # min_vis = 1000000
#     # agg_vis = 0
#
#     # max_uv = 0
#     # min_uv = 1000000
#     # agg_uv = 0
#
#     # max_ir = 0
#     # min_ir = 1000000
#     # # agg_ir = 0
#     #
#     # max_x = 0
#     # min_x = 1000000
#     # # agg_x = 0
#     #
#     # max_y = 0
#     # min_y = 1000000
#     # # agg_y = 0
#     #
#     # max_z = 0
#     # min_z = 1000000
#     # # agg_z = 0
#
#     while cal_count <= cal_trials:
#         # vis = lightSensor.readVisible()
#         # agg_vis += (vis / cal_trials)
#         # max_vis, min_vis = min_max_test(vis, max_vis, min_vis)
#
#         ir = lightSensor.readIR()
#         sq_ir += pow(ir, 2)
#         mean_ir = get_mean(mean_ir, ir, n)
#         # max_ir, min_ir = min_max_test(ir, max_ir, min_ir)
#         # agg_ir += (ir/cal_trials)
#
#         # uv = lightSensor.readUV()   # need to divide UV by 100 to get the index
#         # max_uv, min_uv = min_max_test(uv, max_uv, min_uv)
#         # agg_uv += (uv/cal_trials)
#
#         x = round(agSensor.getX(), 5)
#         sq_x += pow(x, 2)
#         mean_x = get_mean(mean_x, x, n)
#         # max_x, min_x = min_max_test(x, max_x, min_x)
#         # agg_x += (x/cal_trials)
#
#         y = round(agSensor.getY(), 5)
#         sq_y += pow(y, 2)
#         mean_y = get_mean(mean_y, y, n)
#         # max_y, min_y = min_max_test(y, max_y, min_y)
#         # agg_y += (y/cal_trials)
#
#         z = round(agSensor.getZ(), 5)
#         sq_z += pow(z, 2)
#         mean_z = get_mean(mean_z, z, n)
#         # max_z, min_z = min_max_test(z, max_z, min_z)
#         # agg_z += (z/cal_trials)
#
#         if (n % 25) == 0:
#             print("Trial count:", cal_count)
#         n += 1
#
#         time.sleep(0.001)
#
#     mean_array = np.array([mean_ir, mean_x, mean_y, mean_z])
#     print("Mean array:", mean_array)
#
#     # max_array = np.array([max_vis, max_ir, max_uv,
#     #                       max_x, max_y, max_z])
#     # print("Max array:", max_array)
#     #
#     # min_array = np.array([min_vis, min_ir, min_uv,
#     #                       min_x, min_y, min_z])
#     # print("Min array:", min_array)
#     #
#     # range_array = np.array([(max_vis - min_vis),
#     #                         (max_ir - min_ir),
#     #                         (max_uv - min_uv),
#     #                         (max_x - min_x),
#     #                         (max_y - min_y),
#     #                         (max_z - min_z)])
#
#     sd_array = np.array([get_variance(mean_ir, sq_ir, n),
#                          get_variance(mean_x, sq_x, n),
#                          get_variance(mean_y, sq_y, n),
#                          get_variance(mean_z, sq_z, n)])
#     print("SD array:", sd_array)
#
#     return mean_array, sd_array

# meanArray, maxArray, minArray, rangeArray = norm_calibration()
# meanArray, sdArray = norm_calibration()

print("Parameters for calibration extracted.")

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
while True:
    ir = ir_weight*1.47*log(lightSensor.readIR())
    max_array[0], min_array[0], update_med = min_max_test(ir,
                                                        max_array[0],
                                                        min_array[0])
    if update_med:
        med_array[0] = (max_array[0] + min_array[0])/2
    scaled_ir = ((ir - med_array[0])/(max_array[0] - min_array[0])) + 0.5
    scaled_ir = (1-ir_weight)*current_ir + ir_weight*128*scaled_ir
    if abs(current_ir - scaled_ir) >= 8:
        current_ir = scaled_ir
        print_ir = current_ir
    else:
        # Only prints non-zero value when there has been a large change in the value of ir
        print_ir = 0

    x = agSensor.getX()
    max_array[1], min_array[1], update_med = min_max_test(x,
                                                          max_array[1],
                                                          min_array[1])
    if update_med:
        med_array[1] = (max_array[1] + min_array[1])/2
    scaled_x = ((x - med_array[1])/(max_array[1] - min_array[1])) + 0.5
    scaled_x = (1 - x_weight)*current_x + x_weight*128*scaled_x
    if abs(current_x - scaled_x) >= 17:
        current_x = scaled_x
        print_x = current_x
    else:
        print_x = 0

    y = agSensor.getY()
    max_array[2], min_array[2], update_med = min_max_test(y,
                                                          max_array[2],
                                                          min_array[2])
    if update_med:
        med_array[2] = (max_array[2] + min_array[2])/2
    scaled_y = ((y - med_array[2]) / (max_array[2] - min_array[2])) + 0.5
    scaled_y = (1 - y_weight) * current_y + y_weight * 128 * scaled_y
    if abs(current_y - scaled_y) >= 22:
        current_y = scaled_y
        print_y = current_y
    else:
        print_y = 0

    z = agSensor.getZ()
    max_array[3], min_array[3], update_med = min_max_test(z,
                                                          max_array[3],
                                                          min_array[3])
    if update_med:
        med_array[3] = (max_array[3] + min_array[3])/2
    scaled_z = ((z - med_array[3]) / (max_array[3] - min_array[3])) + 0.5
    scaled_z = (1 - z_weight) * current_z + z_weight * 128 * scaled_z
    if abs(current_z - scaled_z) >= 22:
        current_z = scaled_z
        print_z = current_z
    else:
        print_z = 0

    # data = str(int(print_ir)) + "," + \
    #        str(int(print_x)) + "," + \
    #        str(int(print_y)) + "," + \
    #        str(int(print_z))

    if int(print_ir) != 0 or int(print_x) != 0 or int(print_y) != 0 or int(print_z) != 0:
        data = str(int(print_ir)) + "," + \
               str(int(print_x)) + "," + \
               str(int(print_y)) + "," + \
               str(int(print_z))

    # if data:
    #     client_socket.send(data)
    #     currentTime = datetime.datetime.now()
    #     print("Message sent at:", currentTime)

    sleep(0.01)





