
from Adafruit_GPIO import I2C
import RPi.GPIO as GPIO  # needed for Hardware interrupt


class AccGyro:

    # I2C
    i2c = None
    I2C_ADDRESS_1 = 0x18
    I2C_ADDRESS_2 = 0x19
    # Default
    I2C_DEFAULT = I2C_ADDRESS_1

    # Bus
    BUS_NUMBER = 1  # -1

    # Ranges
    RANGE_2G  = 0b00  # default
    RANGE_4G  = 0b01
    RANGE_8G  = 0b10
    RANGE_16G = 0b11

    # Defaults
    RANGE_DEFAULT = RANGE_2G
    DATARATE_DEFAULT = DATARATE_400HZ = 0b0111

    # Registers
    REG_WHOAMI        = 0x0F  # Device identification register

    # Registers - Control
    REG_CTRL1         = 0x20  # Used for data rate selection, and enabling/disabling individual axis
    REG_CTRL2         = 0x21
    REG_CTRL3         = 0x22
    REG_CTRL4         = 0x23  # Used for BDU, scale selection, resolution selection and self-testing
    REG_CTRL5         = 0x24
    REG_CTRL6         = 0x25

    # Read Register Data
    REG_OUT_X_L       = 0x28
    REG_OUT_X_H       = 0x29
    REG_OUT_Y_L       = 0x2A
    REG_OUT_Y_H       = 0x2B
    REG_OUT_Z_L       = 0x2C
    REG_OUT_Z_H       = 0x2D

    # Registers Clicking
    REG_INT1CFG       = 0x30
    REG_INT1SRC       = 0x31
    REG_INT1THS       = 0x32
    REG_INT1DUR       = 0x33
    REG_CLICKCFG      = 0x38
    REG_CLICKSRC      = 0x39
    REG_CLICKTHS      = 0x3A

    # Registers Timing
    REG_TIMELIMIT     = 0x3B
    REG_TIMELATENCY   = 0x3C
    REG_TIMEWINDOW    = 0x3D

    # Values
    DEVICE_ID  = 0x33
    INT_IO     = 0x04  # GPIO pin for interrupt
    CLK_NONE   = 0x00
    CLK_SINGLE = 0x01
    CLK_DOUBLE = 0x02

    AXIS_X = 0x00
    AXIS_Y = 0x01
    AXIS_Z = 0x02

    # changed busnumber to 1 (from -1)
    # alternative i2c address=0x19
    def __init__(self, address=I2C_DEFAULT, bus=BUS_NUMBER,
                 g_range=RANGE_DEFAULT, datarate=DATARATE_DEFAULT,
                 debug=False):
        self.isDebug = debug
        self.debug("Initialising LIS3DH")

        # self.i2c = Adafruit_I2C(address, busnum=bus)
        self.i2c = I2C.Device(address, busnum=bus)
        self.address = address

        try:
            val = self.i2c.readU8(self.REG_WHOAMI)
            if val != self.DEVICE_ID:
                raise Exception(("Device ID incorrect - expected 0x{:x}, " +
                                 "got 0x{:x} at address 0x{:x}").format(self.DEVICE_ID, val, self.address))

            self.debug(("Successfully connected to LIS3DH " +
                        "at address 0x{:x}").format(self.address))
        except Exception as e:
            print("Error establishing connection with LIS3DH")
            print(e)

        # Enable all axis
        self.setAxisStatus(self.AXIS_X, True)
        self.setAxisStatus(self.AXIS_Y, True)
        self.setAxisStatus(self.AXIS_Z, True)

        # Set refresh rate (default: 400Hz)
        self.setDataRate(datarate)

        self.setHighResolution()
        self.setBDU()

        self.setRange(g_range)

    # Get reading from X axis
    def getX(self):
        return self.getAxis(self.AXIS_X)

    # Get reading from Y axis
    def getY(self):
        return self.getAxis(self.AXIS_Y)

    # Get reading from Z axis
    def getZ(self):
        return self.getAxis(self.AXIS_Z)

    # Get a reading from the desired axis
    def getAxis(self, axis):
        # Determine which register we need to read from (2 per axis)
        base = self.REG_OUT_X_L + (2 * axis)

        # Read the low and high registers, combine and 2s compliment
        res = self.i2c.readU8(base) | (self.i2c.readU8(base + 1) << 8)
        res = self.twosComp(res)

        # Fetch the set range
        g_range = self.getRange()
        divisor = 1
        if g_range == self.RANGE_2G:
            divisor = 16380
        elif g_range == self.RANGE_4G:
            divisor = 8190
        elif g_range == self.RANGE_8G:
            divisor = 4096
        elif g_range == self.RANGE_16G:
            divisor = 1365.33

        return float(res) / divisor

    # Get the sensor's dynamic range
    def getRange(self):

        # Read register, remove lowest 4 bits and mask
        val = (self.i2c.readU8(self.REG_CTRL4) >> 4)
        val &= 0b0011

        if val == self.RANGE_2G:
            return self.RANGE_2G
        elif val == self.RANGE_4G:
            return self.RANGE_4G
        elif val == self.RANGE_8G:
            return self.RANGE_8G
        else:
            return self.RANGE_16G

    # Set the range of the sensor
    def setRange(self, g_range):
        if g_range < 0 or g_range > 3:
            raise Exception("Tried to set invalid range")

        # Read/Empty Register and replace with new range, write back to the same register
        val = self.i2c.readU8(self.REG_CTRL4)
        val &= ~(0b110000)
        val |= (g_range << 4)
        self.writeRegister(self.REG_CTRL4, val)


    def setAxisStatus(self, axis, enable):
        if axis < 0 or axis > 2:
            raise Exception("Tried to modify invalid axis")

        # Modify CTRL_REG1 to enable or disable an axis, read then write over with the new command
        current = self.i2c.readU8(self.REG_CTRL1)
        status = 1 if enable else 0
        final = self.setBit(current, axis, status)
        self.writeRegister(self.REG_CTRL1, final)

    # Set up waiting GPIO interrupts
    def setInterrupt(self, mycallback):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.INT_IO, GPIO.IN)
        GPIO.add_event_detect(self.INT_IO, GPIO.RISING, callback=mycallback)

    def setClick(self, clickmode, clickthresh=80, timelimit=10, timelatency=20, timewindow=100, mycallback=None):

        # Valid escape for undefined click mode
        if (clickmode == self.CLK_NONE):
            val = self.i2c.readU8(self.REG_CTRL3)
            val &= ~(0x80)
            self.writeRegister(self.REG_CTRL3, val)
            self.writeRegister(self.REG_CLICKCFG, 0)
            return

        # Read out click registers
        self.writeRegister(self.REG_CTRL3, 0x80)
        self.writeRegister(self.REG_CTRL5, 0x08)

        # Write new commands to click registers, all axes active
        # Single tap
        if (clickmode == self.CLK_SINGLE):
            self.writeRegister(self.REG_CLICKCFG, 0x15)
        # Double tap
        if (clickmode == self.CLK_DOUBLE):
            # turn on all axes & doubletap
            self.writeRegister(self.REG_CLICKCFG, 0x2A)

        # set timing parameters
        self.writeRegister(self.REG_CLICKTHS, clickthresh)
        self.writeRegister(self.REG_TIMELIMIT, timelimit)
        self.writeRegister(self.REG_TIMELATENCY, timelatency)
        self.writeRegister(self.REG_TIMEWINDOW, timewindow)

        # Ref appropriate GPIO interrupt
        if mycallback is not None:
            self.setInterrupt(mycallback)

    # Read out click registers
    def getClick(self):
        reg = self.i2c.readU8(self.REG_CLICKSRC)  # read click register
        self.i2c.readU8(self.REG_INT1SRC)         # reset interrupt flag
        return reg

    # Data rate defined in public part of class
    def setDataRate(self, dataRate):
        val = self.i2c.readU8(self.REG_CTRL1)
        val &= 0b1111
        val |= (dataRate << 4)
        self.writeRegister(self.REG_CTRL1, val)

    # Set high resolution
    def setHighResolution(self, highRes=True):
        # Read out registers
        val = self.i2c.readU8(self.REG_CTRL4)
        status = 1 if highRes else 0

        # High resolution is bit 4 of REG_CTRL4
        final = self.setBit(val, 3, status)
        self.writeRegister(self.REG_CTRL4, final)

    def setBDU(self, bdu=True):
        val = self.i2c.readU8(self.REG_CTRL4)  # Get current value
        status = 1 if bdu else 0

        # Block data update is bit 8 of REG_CTRL4
        final = self.setBit(val, 7, status)
        self.writeRegister(self.REG_CTRL4, final)

    # Write the given value to the given register
    def writeRegister(self, register, value):
        self.debug("WRT {} to register 0x{:x}".format(bin(value), register))self.i2c.write8(register, value)

    # Helper function to assist multiple read/write processes
    def setBit(self, input, bit, value):
        mask = 1 << bit
        input &= ~mask
        if value:
            input |= mask
        return input

    def twosComp(self, x):
        if (0x8000 & x):
            x = - (0x010000 - x)
        return x

    # Print an output of all registers to empty
    def dumpRegisters(self):
        for x in range(0x0, 0x3D):
            read = self.i2c.readU8(x)
            print("{:x}: {}".format(x, bin(read)))

    def debug(self, message):
        if not self.isDebug:
            return
        print(message)
