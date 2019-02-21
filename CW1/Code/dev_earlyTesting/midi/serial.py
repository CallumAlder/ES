import serial
import time

ser = serial.Serial("COM9", baudrate=9600, timeout=1)
# change first parameter to "arduino serial port" (e.g."COM4"), found in arduino software -> Tools -> Port
time.sleep(0.3)