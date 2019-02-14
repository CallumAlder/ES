import serial
import RPi.GPIO as GPIO
from time import sleep

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

GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering  
GPIO.setup(4, GPIO.IN)    # set GPIO25 as input (button)  
  
# Define a threaded callback function to run in another thread when events are detected  
def my_callback(channel):  
    if GPIO.input(4):     # if port 25 == 1  
        print ("Rising edge detected on 4") 
    else:                  # if port 25 != 1  
        print ("Falling edge detected on 4")  
  
# when a changing edge is detected on port 25, regardless of whatever   
# else is happening in the program, the function my_callback will be run  
GPIO.add_event_detect(4, GPIO.BOTH, callback=my_callback) 

while 1:

