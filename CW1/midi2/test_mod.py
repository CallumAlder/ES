import serial
from time import sleep
import pigpio

# Set MIDI port
ser = serial.Serial('/dev/ttyAMA0', baudrate=38400)  # Open serial at 38400bps

#msg = str.encode('B11D3F)'
#for ii in msg:
#    print(ii,":",chr(ii))

#outmidi = [i for i in msg]
#print("outmidi: ", outmidi)

#ser.write(outmidi)

#msg = bytearray([176,29,63])
#ser.write(msg)




#pi1 = pigpio.pi()
#buttPin = 4
#pi1.set_mode(buttPin, pigpio.INPUT)


#def buttonDown(gpio, level, tick):
#    print("DOWN")
#    ser.write(msg)
    #outport.send(onmess)


#def buttonUp(gpio, level, tick):
#    print("UP")
    #outport.send(offmess)


#cb = pi1.callback(buttPin, pigpio.RISING_EDGE, buttonDown)
#cb2 = pi1.callback(buttPin, pigpio.FALLING_EDGE, buttonUp)
# Just loop and do nothing
while True:
    ser.write(bytearray([176,29,63]))
    sleep(2)
    ser.write(bytearray([176,29,31]))
    sleep(2)
