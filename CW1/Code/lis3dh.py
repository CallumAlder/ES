# The MIT License (MIT)
#
# Copyright (c) 2018 Skadoosh
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`lis3dh`
====================================================

I2C driver for the LIS3DH contactless IR thermometer

* Author(s): XYZ 
TODO

Implementation Notes
--------------------

**Hardware:**

**Software and Dependencies:**


"""
''' LIS3DH library for MicroPython
    LIS3DH: a triple-axis accelerometer
    register size: 8 bits
'''



#//////////////////// imports /////////////////////////////////////////////////
from machine import Pin, I2C
import utime
import ujson
import math



#//////////////////// constants ///////////////////////////////////////////////
# register addresses etc.
LIS3DH_DEFAULT_ADDRESS  = 0x18 # default I2C address. If SDO/SA0 is 3V -> 0x19
LIS3DH_DEVICE_ID        = 0x33 # expected device ID value in LIS3DH_REG_WHOAMI

LIS3DH_REG_STATUS1      = 0x07 # registers
LIS3DH_REG_OUTADC1_L    = 0x08
LIS3DH_REG_OUTADC1_H    = 0x09
LIS3DH_REG_OUTADC2_L    = 0x0A
LIS3DH_REG_OUTADC2_H    = 0x0B
LIS3DH_REG_OUTADC3_L    = 0x0C
LIS3DH_REG_OUTADC3_H    = 0x0D
LIS3DH_REG_INTCOUNT     = 0x0E
LIS3DH_REG_WHOAMI       = 0x0F # stores device ID (for checking sensor connected)
LIS3DH_REG_TEMPCFG      = 0x1F
LIS3DH_REG_CTRL1        = 0x20
LIS3DH_REG_CTRL2        = 0x21
LIS3DH_REG_CTRL3        = 0x22
LIS3DH_REG_CTRL4        = 0x23
LIS3DH_REG_CTRL5        = 0x24
LIS3DH_REG_CTRL6        = 0x25
LIS3DH_REG_REFERENCE    = 0x26
LIS3DH_REG_STATUS2      = 0x27
LIS3DH_REG_OUT_X_L      = 0x28 # X-axis low byte
LIS3DH_REG_OUT_X_H      = 0x29 # X-axis high byte
LIS3DH_REG_OUT_Y_L      = 0x2A
LIS3DH_REG_OUT_Y_H      = 0x2B
LIS3DH_REG_OUT_Z_L      = 0x2C
LIS3DH_REG_OUT_Z_H      = 0x2D
LIS3DH_REG_FIFOCTRL     = 0x2E
LIS3DH_REG_FIFOSRC      = 0x2F
LIS3DH_REG_INT1CFG      = 0x30
LIS3DH_REG_INT1SRC      = 0x31
LIS3DH_REG_INT1THS      = 0x32
LIS3DH_REG_INT1DUR      = 0x33
LIS3DH_REG_CLICKCFG     = 0x38
LIS3DH_REG_CLICKSRC     = 0x39
LIS3DH_REG_CLICKTHS     = 0x3A
LIS3DH_REG_TIMELIMIT    = 0x3B
LIS3DH_REG_TIMELATENCY  = 0x3C
LIS3DH_REG_TIMEWINDOW   = 0x3D
LIS3DH_REG_ACTTHS       = 0x3E
LIS3DH_REG_ACTDUR       = 0x3F

LIS3DH_RANGE_16_G       = 0b11 # range. +/- 16g
LIS3DH_RANGE_8_G        = 0b10 # +/- 8g
LIS3DH_RANGE_4_G        = 0b01 # +/- 4g
LIS3DH_RANGE_2_G        = 0b00 # +/- 2g (default)

LIS3DH_AXIS_X           = 0x0  # axis
LIS3DH_AXIS_Y           = 0x1
LIS3DH_AXIS_Z           = 0x2

# data rate: for setting bandwidth
LIS3DH_DATARATE_400_HZ          = 0b0111 # 400Hz
LIS3DH_DATARATE_200_HZ          = 0b0110 # 200Hz
LIS3DH_DATARATE_100_HZ          = 0b0101 # 100Hz
LIS3DH_DATARATE_50_HZ           = 0b0100 # 50Hz
LIS3DH_DATARATE_25_HZ           = 0b0011 # 25Hz
LIS3DH_DATARATE_10_HZ           = 0b0010 # 10Hz
LIS3DH_DATARATE_1_HZ            = 0b0001 # 1Hz
LIS3DH_DATARATE_POWERDOWN       = 0
LIS3DH_DATARATE_LOWPOWER_1K6HZ  = 0b1000
LIS3DH_DATARATE_LOWPOWER_5KHZ   = 0b1001




#//////////////////// variables ///////////////////////////////////////////////
_i2c_addr = LIS3DH_DEFAULT_ADDRESS
_i2c_port = I2C(scl = Pin(5), sda = Pin(4), freq = 400000)

range_g = 0 # sensor range as +/- *g
divider = 1 # depends on range. Acceleration in g = sensor data / divider

global_distance = 0
global_steps = 0
step_timer_start = utime.time()




#//////////////////// parameters //////////////////////////////////////////////

# CLICK_THRESHOLD: adjust this number for the sensitivity of the 'click' force
#   this strongly depends on the range
#   16G: 5-10, 8G: 10-20, 4G: 20-40, 2G: 40-80
CLICK_THRESHOLD = 80

ACCEL_NUM_SAMPLES = 10
ACCEL_READ_INTERVAL = 0.1
ACCEL_STATIONARY_MARGIN = 0.1

STEP_THRESHOLD = 1.4                    # unit: mm s^-2. For step detection
STEP_MAX_RPM = 180                      # max assumed cadence
# STEP_MIN_INTERVAL: the minimum cooldown time between consecutive steps to
#   avoid detecting 1 steps as many step (due to vibration etc.)
#   unit: second
STEP_MIN_INTERVAL = 60 / STEP_MAX_RPM



#//////////////////// functions ///////////////////////////////////////////////

## "private" functions

def begin_i2c():                                # begin I2C communication
    print("Begin I2C communication...")

    device_id = read_mem_8(LIS3DH_REG_WHOAMI)
    #print('LIS3DH device_id: {0}'.format(hex(device_id)))

    if device_id != LIS3DH_DEVICE_ID:
        print("FAILURE: LIS3DH not detected at address {0}".format(hex(_i2c_addr)))
        return False                            # sensor not found
    else:
        print("SUCCESS: LIS3DH detected at {0}".format(hex(_i2c_addr)))
        write_mem_8(LIS3DH_REG_CTRL1, 0x07)     # enable all axes, normal mode
        set_data_rate(LIS3DH_DATARATE_400_HZ)   # 400Hz rate
        write_mem_8(LIS3DH_REG_CTRL4, 0x88)     # high res & BDU enabled
        write_mem_8(LIS3DH_REG_CTRL3, 0x10)     # DRDY on INT1
        write_mem_8(LIS3DH_REG_TEMPCFG, 0x80)   # enable adcs
        return True                             # sensor found and initialised

def set_data_rate(data_rate):
    ctl1 = read_mem_8(LIS3DH_REG_CTRL1)
    ctl1 &= ~(0xF0) # mask off bits
    ctl1 |= (data_rate << 4)
    write_mem_8(LIS3DH_REG_CTRL1, ctl1)

def get_accel():                            # read x y z at once
    # read data
    x_MSB = read_mem_8(LIS3DH_REG_OUT_X_H)  # read x high byte register
    x_LSB = read_mem_8(LIS3DH_REG_OUT_X_L)  # read x low byte register
    y_MSB = read_mem_8(LIS3DH_REG_OUT_Y_H)
    y_LSB = read_mem_8(LIS3DH_REG_OUT_Y_L)
    z_MSB = read_mem_8(LIS3DH_REG_OUT_Z_H)
    z_LSB = read_mem_8(LIS3DH_REG_OUT_Z_L)

    # calculation
    global global_vel_x
    global global_vel_y
    global global_vel_z
    global global_dist_x
    global global_dist_y
    global global_dist_z

    accel_x = (uint16_to_int16((x_MSB << 8) | (x_LSB))/divider)
    accel_y = (uint16_to_int16((y_MSB << 8) | (y_LSB))/divider)
    accel_z = (uint16_to_int16((z_MSB << 8) | (z_LSB))/divider)
    accel_mag = get_xyz_mag(accel_x, accel_y, accel_z)

    # compile data
    data = {}
    data['mag'] = accel_mag

    return data

def set_click(c, click_thresh, time_limit = 10, time_latency = 20, time_window = 255):
    if c == 0:          # disable int
        r = read_mem_8(LIS3DH_REG_CTRL3)
        r &= ~(0x80)    # turn off I1_CLICK
        write_mem_8(LIS3DH_REG_CTRL3, r)
        write_mem_8(LIS3DH_REG_CLICKCFG, 0)
    else:
        write_mem_8(LIS3DH_REG_CTRL3, 0x80) # turn on int1 click
        write_mem_8(LIS3DH_REG_CTRL5, 0x08) # latch interrupt on int1
        if c == 1:
            write_mem_8(LIS3DH_REG_CLICKCFG, 0x15) # turn on all axes & single-click
        elif c == 2:
            write_mem_8(LIS3DH_REG_CLICKCFG, 0x2A) # turn on all axes & double-click

        write_mem_8(LIS3DH_REG_CLICKTHS, click_thresh)      # arbitrary
        write_mem_8(LIS3DH_REG_TIMELIMIT, time_limit)       # arbitrary
        write_mem_8(LIS3DH_REG_TIMELATENCY, time_latency)   # arbitrary
        write_mem_8(LIS3DH_REG_TIMEWINDOW, time_window)     # arbitrary

def get_click_raw():
    return read_mem_8(LIS3DH_REG_CLICKSRC)

def get_click():
    # read data
    dclick = False
    sclick = False
    x = False
    y = False
    z = False

    raw = get_click_raw()
    if (raw & 0x20):
        dclick = True   # double-click
    if (raw & 0x10):
        sclick = True   # single-click
    if (raw & 0x01):
        x = True        # x-axis high
    if (raw & 0x02):
        y = True        # y-axis high
    if (raw & 0x04):
        z = True        # z-axis high

    # compile data
    data = {}
    data['dclick'] = dclick
    data['sclick'] = sclick
    data['x'] = x
    data['y'] = y
    data['z'] = z

    return data

def uint16_to_int16(uint16):
    result = uint16
    if result > 32767:
        result -= 65536
    return result

def set_range(range = 2):   # range = 2,4,8 or 16
    r = LIS3DH_RANGE_2_G    # default
    if range == 4:
        r = LIS3DH_RANGE_4_G
    elif range == 8:
        r = LIS3DH_RANGE_8_G
    elif range == 16:
        r = LIS3DH_RANGE_16_G
    reg_data = read_mem_8(LIS3DH_REG_CTRL4)
    reg_data &= ~(0x30)
    reg_data |= r << 4
    write_mem_8(LIS3DH_REG_CTRL4, reg_data)

def get_range():        # read the data format register to preserve bits
    r = read_mem_8(LIS3DH_REG_CTRL4)
    r = (r >> 4) & 0x03
    return r

def get_xyz_mag(x, y, z): # return magnitude of a 3D vector
    return math.pow(x, 2) + math.pow(y, 2) + math.pow(z, 2)

def init_all_param():   # initialise all global parameters
    global divider
    global range_g
    range = get_range()
    if (range == LIS3DH_RANGE_16_G):
        range_g = 16
        divider = 1365  # different sensitivity at 16g
    if (range == LIS3DH_RANGE_8_G):
        range_g = 8
        divider = 4096
    if (range == LIS3DH_RANGE_4_G):
        range_g = 4
        divider = 8190
    if (range == LIS3DH_RANGE_2_G):
        range_g = 2
        divider = 16380

def write_mem_8(reg_addr, data):
    _i2c_port.writeto_mem(_i2c_addr, reg_addr, bytearray([data]))

def read_mem(reg_addr, nbytes):
    str = _i2c_port.readfrom_mem(_i2c_addr, reg_addr, nbytes)
    result = 0
    counter = 0
    for char in str:
        result = result << counter | char
        counter += 8
    return result

def read_mem_8(reg_addr):
    return read_mem(reg_addr, 1)

def addr_detected():
    if _i2c_addr in _i2c_port.scan():
        return True
    else:
        return False

# "public" functions

def init(range, ct):
    if not addr_detected():
        return False
    else:
        begin_i2c()
        set_range(range)
        set_click(2, click_thresh = ct)
        init_all_param()
        return True

def get_steps():
    # read raw data
    raw_data = {}
    raw_data['accel'] = get_accel()       # read x,y,z acceleration

    # calculation (step detection)
    global global_distance
    global global_steps
    global step_timer_start
    if step_detected(raw_data) == True and utime.time() - step_timer_start >= STEP_MIN_INTERVAL:
        global_steps += 1
        step_timer_start = utime.time()  # reset step timer

    return global_steps

def step_detected(data):     # return number of steps
    return data['accel']['mag'] >= STEP_THRESHOLD