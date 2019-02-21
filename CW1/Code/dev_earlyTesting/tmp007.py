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
`tmp007`
====================================================

I2C driver for the TMP007 contactless IR thermometer

* Author(s): XYZ 
TODO

Implementation Notes
--------------------

**Hardware:**

**Software and Dependencies:**


"""
''' TMP007 library for MicroPython
    TMP007: a contact-less infrared thermopile temperature sensor that can
        measure temperature without touching the subject
    register size: 16 bits
'''



#//////////////////// imports ////////////////////
from machine import Pin, I2C



#//////////////////// constants ////////////////////
TMP007_VOBJ         = 0x00
TMP007_TDIE         = 0x01
TMP007_CONFIG       = 0x02
TMP007_TOBJ         = 0x03
TMP007_STATUS       = 0x04
TMP007_STATMASK     = 0x05

TMP007_CFG_RESET    = 0x8000
TMP007_CFG_MODEON   = 0x1000
TMP007_CFG_1SAMPLE  = 0x0000
TMP007_CFG_2SAMPLE  = 0x0200
TMP007_CFG_4SAMPLE  = 0x0400
TMP007_CFG_8SAMPLE  = 0x0600
TMP007_CFG_16SAMPLE = 0x0800
TMP007_CFG_ALERTEN  = 0x0100
TMP007_CFG_ALERTF   = 0x0080
TMP007_CFG_TRANSC   = 0x0040

TMP007_STAT_ALERTEN = 0x8000
TMP007_STAT_CRTEN   = 0x4000

TMP007_I2CADDR              = 0x40  # default I2C address
TMP007_REG_DEVICE_ID        = 0x1F  # register storing the device ID
TMP007_DEVICE_ID            = 0x78



#//////////////////// variables ////////////////////
_i2c_addr = TMP007_I2CADDR
_i2c_port = I2C(scl = Pin(5), sda = Pin(4), freq = 400000)

samplerate = TMP007_CFG_16SAMPLE # high resolution


#//////////////////// functions ////////////////////
## "private" functions
# begin I2C communication
def begin_i2c():
    print("Begin I2C communication...")

    device_id = read_mem_16(TMP007_REG_DEVICE_ID)
    #print('TMP007 device_id: {0}'.format(hex(device_id)))

    if device_id != TMP007_DEVICE_ID:
        print("FAILURE: TMP007 not detected at address {0}".format(hex(_i2c_addr)))
        return False    # sensor not found
    else:
        print("SUCCESS: TMP007 detected at {0}".format(hex(_i2c_addr)))

        config = TMP007_CFG_MODEON | TMP007_CFG_ALERTEN | TMP007_CFG_TRANSC | samplerate
        stat_mask = TMP007_STAT_ALERTEN | TMP007_STAT_CRTEN

        write_mem_16(TMP007_CONFIG, config)
        write_mem_16(TMP007_STATMASK, stat_mask)

        return True     # sensor found and initialised

def uint16_to_int16(uint16):
    result = uint16
    if result > 32767:
        result -= 65536
    return result

def write_mem_16(reg_addr, data):    # write 16 bits to register
    _i2c_port.writeto_mem(_i2c_addr, reg_addr, bytearray([data >> 8, data]))

def read_mem(reg_addr, nbytes):
    str = _i2c_port.readfrom_mem(_i2c_addr, reg_addr, nbytes)
    result = 0
    counter = 0
    for char in str:
        result = result << counter | char
        counter += 8
    return result

def read_mem_16(reg_addr):    # write 16 bits to register
    return read_mem(reg_addr, 2)

def addr_detected():
    if _i2c_addr in _i2c_port.scan():
        return True
    else:
        return False

## "public" functions
def init():
    if not addr_detected():
        return False
    else:
        begin_i2c()
        return True

def read_die_temp_c():
    raw = read_mem_16(TMP007_TDIE)
    #if (raw & 0x1): # invalid temperature
        #return NAN
    raw >>= 2
    t_die = raw * 0.03125 # convert to Celsius
    return uint16_to_int16(t_die)
    
def read_obj_temp_c():
    raw = read_mem_16(TMP007_TOBJ)
    raw >>= 2
    t_obj = raw * 0.03125 # convert to Celsius
    return uint16_to_int16(t_obj)