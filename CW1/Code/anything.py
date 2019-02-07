'''
import si1145 as iig
import json

sensor = iig.SI1145()

print(sensor)
print("iig")
print("iig")
print("iig")

ir = sensor.readIR()
uv = sensor.readUV()
vis = sensor.readVisible()
# prox = sensor.readProx()

data = {"IR": ir, "UV": uv, "Visible": vis}
print(data)
package = json.dumps(data)

# do another thing and then push it
# pusha T
# pushed again gg
'''

import paho.mqtt as mqtt

client = mqtt.Client(client_id="skad00sh")

if client.connect("iot.eclipse.org", port=443) == 0:
    mqtt.error_string(client.publish("hworld", "msg").rc)

