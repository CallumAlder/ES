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

def on_publish(client, userdata, mid):
   print("mid: "+ str(mid))

def on_message(client, userdata, msg):
   msg = str(msg.payload.decode())
   print("msg: " + msg)
   return msg
   # print(client.__dict__)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("$SYS/#")
    # client.subscribe("EdB/A")
    client.subscribe("IC.embedded/skadoosh/midi")


broker = "iot.eclipse.org"

# broker = "localhost"; port = 1883
# broker = "test.mosquitto.org"; port = 1883
port = 1883

# client = mqtt.Client(client_id="skad00sh")
client = mqtt.Client()
client.on_publish = on_publish
client.on_message = on_message
client.on_connect = on_connect

# client.tls_set(ca_certs="mosquitto.org.crt",
#                certfile="client.crt",
#                keyfile="client.key")
# client.tls_set("eclipse-cert.pem",tls_version=ssl.PROTOCOL_TLSv1_2)

X = client.connect(broker, port=port)
print(X)
if X == 0:

    client.loop_start()
    while 1:
        # client.on_publish = on_publish
        # client.on_message = on_message
        # client.on_connect = on_connect

        # print("Subscribing...")

        # client.subscribe("BRX/EdB/")
        # client.subscribe("hworld")
        # client.subscribe("EdB/A")
        # time.sleep(0.5)

        # client.subscribe("hworld")
        time.sleep(0.5)

        # print("Publishing...")
        # client.publish(topic="IC.embedded/skadoosh/midi", payload="Ife-12/2/2019", qos=1)
        # print(mqtt.error_string(client.publish(topic="IC.embedded/skadoosh/midi", payload=b'test-msg', qos=1).rc))

        time.sleep(2)

    client.loop_stop()
    client.disconnect()
else:
    print("Pas de connexion")
