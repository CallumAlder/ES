import serial
from time import sleep

import pigpio

# Set MIDI port
#ser = serial.Serial('/dev/ttyAMA0', 
#baudrate=38400, 
#parity='N',
#stopbits=0)  # Open serial at 38400bps

#msg = str.encode('B11D3F)'
#for ii in msg:
#    print(ii,":",chr(ii))

#outmidi = [i for i in msg]
#print("outmidi: ", outmidi)

#ser.write(outmidi)

#msg = bytearray([27,63])
#ser.write(msg)




pi1 = pigpio.pi()
buttPin = 4
pi1.set_mode(buttPin, pigpio.INPUT)


def buttonDown(gpio, level, tick):
    print("DOWN")
    #outport.send(onmess)


def buttonUp(gpio, level, tick):
    print("UP")
    #outport.send(offmess)


cb = pi1.callback(buttPin, pigpio.RISING_EDGE, buttonDown)
cb2 = pi1.callback(buttPin, pigpio.FALLING_EDGE, buttonUp)
# Just loop and do nothing
while True:
    pass



while 1:

