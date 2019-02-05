#!/usr/bin/python


# Author: Joe Gutting
# SI1145 library
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
`si1145`
====================================================

Driver for the Si1145/46/47, Infrared Promximity, UV Index and Ambient Light sensor

* Author(s):

Implementation Notes
--------------------
* The Si1145 does not contain LEDs 2 and 3. LED 1 is assumed to be connected to 
  an IR LED
* Using Forced Measurement Mode - i.e. the host specifically requests measurement
  MEAS_RATE = 0

**Hardware:**
Si114

**Software and Dependencies:**

* MicroPython machine library
  pip3 install micropython-machine
* 
"""

import logging
import time

import Adafruit_GPIO.I2C as I2C

# COMMANDS
    # NOTE: These wake the internal sequencer
    # ABCD WXYZ : 1st and 2nd 4 bits
    # 1st 4 bits are supposed to be zero, unless error
    # 2nd 4 bits are a circular counter - incremented each time a command has completed
        # clear with NOP command
SI1145_PARAM_QUERY                      = 0x08  # Reads Param specified by [4:0] bitfield
SI1145_PARAM_SET                        = 0xA0  # Sets Param specified by [4:0] bitfield
SI1145_NOP                              = 0x00  # Resets the Response Register
SI1145_RESET                            = 0x01  # Softare Rest of Firmware
SI1145_BUSADDR                          = 0x02  # Modified i2C Addr
SI1145_PS_FORCE                         = 0x05  # Force a single PS measurement
SI1145_ALS_FORCE                        = 0x06  # Force a single ALS
SI1145_PSALS_FORCE                      = 0x07  # Force a single PS & ALS
SI1145_PS_PAUSE                         = 0x09  # Pause autonomous PS
SI1145_ALS_PAUSE                        = 0x0A  # Pause autonomous ALS
SI1145_PSALS_PAUSE                      = 0x0B  # Pause autonomous PS & ALS
SI1145_PS_AUTO                          = 0x0D  # (Re)start autonomous PS loop
SI1145_ALS_AUTO                         = 0x0E  # (Re)start autonomous ALS loop
SI1145_PSALS_AUTO                       = 0x0F  # (Re)start autonomous PS & ALS loop
SI1145_GET_CAL                          = 0x12  # Push calibration data to registers

# Parameters
    # Must use PARAM_QUERY or _SET to access
    # Enable
SI1145_PARAM_I2CADDR                    = 0x00  # [7:0]=i2c address
SI1145_PARAM_CHLIST                     = 0x01  # Data channel enabler
SI1145_PARAM_CHLIST_ENUV                = 0x80  # CHLIST[7]=Enable UV
SI1145_PARAM_CHLIST_ENAUX               = 0x40  # CHLIST[6]=Enable AUX
SI1145_PARAM_CHLIST_ENALSIR             = 0x20  # CHLIST[5]=Enable ALS & IR
SI1145_PARAM_CHLIST_ENALSVIS            = 0x10  # CHLIST[4]=Enable ALS & Visible
SI1145_PARAM_CHLIST_ENPS1               = 0x01  # CHLIST[2]=Enable PS 1
SI1145_PARAM_CHLIST_ENPS2               = 0x02  # CHLIST[1]=Enable PS 2 
SI1145_PARAM_CHLIST_ENPS3               = 0x04  # CHLIST[0]=Enable PS 3

    # PS LED selection 
SI1145_PARAM_PSLED12SEL                 = 0x02  # LED2=[6:4], LED1=[2:0]
SI1145_PARAM_PSLED12SEL_PS2NONE         = 0x00  # 000 - no LED Driven --- LED2
SI1145_PARAM_PSLED12SEL_PS2LED1         = 0x10  # 001 - LED 1 Driven
SI1145_PARAM_PSLED12SEL_PS2LED2         = 0x20  # 010 - LED 2 Driven
SI1145_PARAM_PSLED12SEL_PS2LED3         = 0x40  # 100 - LED 3 Driven
SI1145_PARAM_PSLED12SEL_PS1NONE         = 0x00  # 000 - no LED Driven --- LED1
SI1145_PARAM_PSLED12SEL_PS1LED1         = 0x01  # 001 - LED 1 Driven
SI1145_PARAM_PSLED12SEL_PS1LED2         = 0x02  # 010 - LED 2 Driven
SI1145_PARAM_PSLED12SEL_PS1LED3         = 0x04  # 100 - LED 3 Driven

SI1145_PARAM_PSLED3SEL                  = 0x03  # [2:0], same idea as above
SI1145_PARAM_PSENCODE                   = 0x05  # [6:4], sets the PS LEDs for the ADC to report
SI1145_PARAM_ALSENCODE                  = 0x06  # [5:4], sets if IR or VIS are reported by the ADC

SI1145_PARAM_PS1ADCMUX                  = 0x07  # Selects ADC input for PS1 \
SI1145_PARAM_PS2ADCMUX                  = 0x08  # Selects ADC input for PS2 | Page 51
SI1145_PARAM_PS3ADCMUX                  = 0x09  # Selects ADC input for PS3 /
SI1145_PARAM_PSADCOUNTER                = 0x0A  # [6:4]=ADC Recovery period - Page 53
SI1145_PARAM_PSADCGAIN                  = 0x0B  # Sets the LED's Pulse width - Page 54
SI1145_PARAM_PSADCMISC                  = 0x0C  # [5]=Set sunlight mode, [2]=RAW ADC or Proximity
SI1145_PARAM_PSADCMISC_RANGE            = 0x20  # 
SI1145_PARAM_PSADCMISC_PSMODE           = 0x04  # 

SI1145_PARAM_ALSIRADCMUX                = 0x0E  # Selects ADC input for ALS_IR
SI1145_PARAM_AUXADCMUX                  = 0x0F  # Selects input for AUX measurement

SI1145_PARAM_ALSVISADCOUNTER            = 0x10  # [6:4] Recovery Period of ADC before ALS-Vis measurement
SI1145_PARAM_ALSVISADCGAIN              = 0x11  # [2:0] Max gain is 128
SI1145_PARAM_ALSVISADCMISC              = 0x12  # [5]=Sets sunlight mode
SI1145_PARAM_ALSVISADCMISC_VISRANGE     = 0x20  # 

SI1145_PARAM_ALSIRADCOUNTER             = 0x1D  # [6:4] Recovery Period of ADC before ALS-IR measurement
SI1145_PARAM_ALSIRADCGAIN               = 0x1E  # [2:0] Max gain is 128
SI1145_PARAM_ALSIRADCMISC               = 0x1F  # [5]=Sets sunglight mode
SI1145_PARAM_ALSIRADCMISC_RANGE         = 0x20  # 

SI1145_PARAM_ADCCOUNTER_511CLK          = 0x70  # 

SI1145_PARAM_ADCMUX_SMALLIR             = 0x00  # Small IR photodiode for SI1145_PARAM_ALSIRADCMUX
SI1145_PARAM_ADCMUX_LARGEIR             = 0x03  # Large IR photodiode for SI1145_PARAM_ALSIRADCMUX


# REGISTERS
SI1145_REG_PARTID                       = 0x00  # 
SI1145_REG_REVID                        = 0x01  # 
SI1145_REG_SEQID                        = 0x02  # 

    # Interrupt
SI1145_REG_INTCFG                       = 0x03  # 
SI1145_REG_INTCFG_INTOE                 = 0x01  # Enable Interrupt Output
SI1145_REG_INTCFG_INTMODE               = 0x02  # 
    # IR Interrupts
SI1145_REG_IRQEN                        = 0x04  # 
SI1145_REG_IRQEN_ALSEVERYSAMPLE         = 0x01  # 
SI1145_REG_IRQEN_PS1EVERYSAMPLE         = 0x04  # 
SI1145_REG_IRQEN_PS2EVERYSAMPLE         = 0x08  # 
SI1145_REG_IRQEN_PS3EVERYSAMPLE         = 0x10  # 


SI1145_REG_IRQMODE1                     = 0x05  # 
SI1145_REG_IRQMODE2                     = 0x06  # 

SI1145_REG_HWKEY                        = 0x07  # 0x17 must be written to this
SI1145_REG_MEASRATE0                    = 0x08  # MEASRATE = [MEARATE1 MEASRATE0] - 16bits
SI1145_REG_MEASRATE1                    = 0x09  # MEASRATE*31.25us = time period between sampling
SI1145_REG_PSRATE                       = 0x0A  # 
SI1145_REG_PSLED21                      = 0x0F  # IR LED current 7:4 = LED2, 3:0 = LED1 - 0000 is min, 1111 is max
SI1145_REG_PSLED3                       = 0x10  # IR LED current 3:0 = LED3
SI1145_REG_UCOEFF0                      = 0x13  # 
SI1145_REG_UCOEFF1                      = 0x14  # 
SI1145_REG_UCOEFF2                      = 0x15  # 
SI1145_REG_UCOEFF3                      = 0x16  # 
SI1145_REG_PARAMWR                      = 0x17  # Mailbox register: passes parameters from host to sequencer
SI1145_REG_COMMAND                      = 0x18  # Mailbox register to internal sequencer - NOTE: wakes the device from standby
SI1145_REG_RESPONSE                     = 0x20  # Response of Command, error when MSB = 1
SI1145_REG_IRQSTAT                      = 0x21  # Interrupt Status: [5]=Command, [4]=PS3, [3]=PS2, [2]=PS1, [1:0]=ALS
SI1145_REG_IRQSTAT_ALS                  = 0x01  # 

SI1145_REG_ALSVISDATA0                  = 0x22  # \
SI1145_REG_ALSVISDATA1                  = 0x23  # | Used in Autonomous measurements
SI1145_REG_ALSIRDATA0                   = 0x24  # | Must be read after INT has 
SI1145_REG_ALSIRDATA1                   = 0x25  # | been asserted, but before 
SI1145_REG_PS1DATA0                     = 0x26  # | the next measurement is made
SI1145_REG_PS1DATA1                     = 0x27  # | Sec 5.6.2 of Docs
SI1145_REG_PS2DATA0                     = 0x28  # |
SI1145_REG_PS2DATA1                     = 0x29  # |
SI1145_REG_PS3DATA0                     = 0x2A  # |
SI1145_REG_PS3DATA1                     = 0x2B  # |
SI1145_REG_UVINDEX0                     = 0x2C  # |
SI1145_REG_UVINDEX1                     = 0x2D  # /
SI1145_REG_PARAMRD                      = 0x2E  # Passes parameteres from sequencer to host
SI1145_REG_CHIPSTAT                     = 0x30  # [2]=RUNNING/awake, [1]=SUSPEND/low-power mode, [0]=SLEEP/lowest power

# I2C Address
SI1145_ADDR                             = 0x60  # 


class SI1145(object):
    """Class to represent a Si1145 UV/Visible/IR Sensor Board.
    """
    def __init__(self, address=SI1145_ADDR, busnum=I2C.get_default_bus()):
        self._logger = logging.getLogger('SI1145')

        # Create I2C device.
        self._device = I2C.Device(address, busnum)

        # reset device
        self._reset()

        # Load calibration values.
        self._load_calibration()

    # device reset
    def _reset(self):
        self._device.write8(SI1145_REG_MEASRATE0, 0)
        self._device.write8(SI1145_REG_MEASRATE1, 0)
        self._device.write8(SI1145_REG_IRQEN, 0)
        self._device.write8(SI1145_REG_IRQMODE1, 0)
        self._device.write8(SI1145_REG_IRQMODE2, 0)
        self._device.write8(SI1145_REG_INTCFG, 0)
        self._device.write8(SI1145_REG_IRQSTAT, 0xFF)

        self._device.write8(SI1145_REG_COMMAND, SI1145_RESET)
        time.sleep(.01)
        self._device.write8(SI1145_REG_HWKEY, 0x17)
        time.sleep(.01)

    # write Param
    def writeParam(self, p, v):
        self._device.write8(SI1145_REG_PARAMWR, v)
        self._device.write8(SI1145_REG_COMMAND, p | SI1145_PARAM_SET)
        paramVal = self._device.readU8(SI1145_REG_PARAMRD)
        return paramVal

    # load calibration to sensor
    def _load_calibration(self):
        # /***********************************/
        # Enable UVindex measurement coefficients!
        self._device.write8(SI1145_REG_UCOEFF0, 0x29)
        self._device.write8(SI1145_REG_UCOEFF1, 0x89)
        self._device.write8(SI1145_REG_UCOEFF2, 0x02)
        self._device.write8(SI1145_REG_UCOEFF3, 0x00)

        # Enable UV sensor
        self.writeParam(SI1145_PARAM_CHLIST, SI1145_PARAM_CHLIST_ENUV | SI1145_PARAM_CHLIST_ENALSIR | SI1145_PARAM_CHLIST_ENALSVIS | SI1145_PARAM_CHLIST_ENPS1)

        # Enable interrupt on every sample
        self._device.write8(SI1145_REG_INTCFG, SI1145_REG_INTCFG_INTOE)
        self._device.write8(SI1145_REG_IRQEN, SI1145_REG_IRQEN_ALSEVERYSAMPLE)

        # /****************************** Prox Sense 1 */

        # Program LED current
        self._device.write8(SI1145_REG_PSLED21, 0x03)  # 20mA for LED 1 only
        self.writeParam(SI1145_PARAM_PS1ADCMUX, SI1145_PARAM_ADCMUX_LARGEIR)

        # Prox sensor #1 uses LED #1
        self.writeParam(SI1145_PARAM_PSLED12SEL, SI1145_PARAM_PSLED12SEL_PS1LED1)

        # Fastest clocks, clock div 1
        self.writeParam(SI1145_PARAM_PSADCGAIN, 0)

        # Take 511 clocks to measure
        self.writeParam(SI1145_PARAM_PSADCOUNTER, SI1145_PARAM_ADCCOUNTER_511CLK)

        # in prox mode, high range
        self.writeParam(SI1145_PARAM_PSADCMISC, SI1145_PARAM_PSADCMISC_RANGE | SI1145_PARAM_PSADCMISC_PSMODE)
        self.writeParam(SI1145_PARAM_ALSIRADCMUX, SI1145_PARAM_ADCMUX_SMALLIR)

        # Fastest clocks, clock div 1
        self.writeParam(SI1145_PARAM_ALSIRADCGAIN, 0)

        # Take 511 clocks to measure
        self.writeParam(SI1145_PARAM_ALSIRADCOUNTER, SI1145_PARAM_ADCCOUNTER_511CLK)

        # in high range mode
        self.writeParam(SI1145_PARAM_ALSIRADCMISC, SI1145_PARAM_ALSIRADCMISC_RANGE)

        # fastest clocks, clock div 1
        self.writeParam(SI1145_PARAM_ALSVISADCGAIN, 0)

        # Take 511 clocks to measure
        self.writeParam(SI1145_PARAM_ALSVISADCOUNTER, SI1145_PARAM_ADCCOUNTER_511CLK)

        # in high range mode (not normal signal)
        self.writeParam(SI1145_PARAM_ALSVISADCMISC, SI1145_PARAM_ALSVISADCMISC_VISRANGE)

        # measurement rate for auto
        self._device.write8(SI1145_REG_MEASRATE0, 0xFF)  # 255 * 31.25uS = 8ms

        # auto run
        self._device.write8(SI1145_REG_COMMAND, SI1145_PSALS_AUTO)

        # returns the UV index * 100 (divide by 100 to get the index)
        def readUV(self):
            return self._device.readU16LE(0x2C)

        # returns visible + IR light levels
        def readVisible(self):
            return self._device.readU16LE(0x22)

        # returns IR light levels
        def readIR(self):
            return self._device.readU16LE(0x24)

        # Returns "Proximity" - assumes an IR LED is attached to LED
        def readProx(self):
            return self._device.readU16LE(0x26)
