#!/usr/bin/python

from lis3dh import AccGyro
from time import sleep


def clickcallback(channel):
    # interrupt handler callback
    print("Interrupt detected")
    click = sensor.getClick()
    print("Click detected (0x%2X)" % (click))
    if (click & 0x10):
        print(" single click")
    if (click & 0x20):
        print(" double click")


if __name__ == '__main__':
    sensor = AccGyro(debug=True)
    sensor.setRange(AccGyro.RANGE_2G)
    sensor.setClick(AccGyro.CLK_DOUBLE, 200, mycallback=clickcallback)

    # second accelerometer
    # s2 = AccGyro(address=0x19, debug=True)

    print("Starting stream")
    while True:

        x = sensor.getX()
        y = sensor.getY()
        z = sensor.getZ()

        # raw values
        print("\rX: %.6f\tY: %.6f\tZ: %.6f" % (x, y, z))
        sleep(0.1)

    # click sensor if polling & not using interrupt
    #        click = sensor.getClick()
    #        if (click & 0x30) :
    #            print "Click detected (0x%2X)" % (click)
    #            if (click & 0x10): print " single click"
#            if (click & 0x20): print " double click"
