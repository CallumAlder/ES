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

import paho.mqtt.client as mqtt
import time

client = mqtt.Client(client_id="skad00sh")

if client.connect("iot.eclipse.org", port=443) == 0:
    client.loop_start()
    print("Subscribing...")
    client.subscribe("hworld")
    time.sleep(0.5)

    print("Publishing...")
    print(mqtt.error_string(client.publish(topic="hworld", payload="msg", qos=1).rc))

    time.sleep(0.5)
    client.loop_stop()
    client.disconnect()

