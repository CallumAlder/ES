# import time
from utime import sleep
import si1145 as SI1145

sensor = SI1145.SI1145()

print('Press Ctrl-Z to cancel')

while True:
        vis = sensor.readVisible()
        IR = sensor.readIR()
        UV = sensor.readUV()
        uvIndex = UV / 100.0
        print('Vis:             ' + str(vis))
        print('IR:              ' + str(IR))
        print('UV Index:        ' + str(uvIndex))
        print('--------')

        time.sleep(0.1)

