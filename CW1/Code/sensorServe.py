import bluetooth
import datetime

import paho.mqtt.client as mqtt
import time

# BT setup
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
bt_port = 1
server_sock.bind(("", bt_port))

# Server listens to accept one connection at a time
server_sock.listen(1)

# server_sock.accept() is a blocking call
client_sock, address = server_sock.accept()
print("Accepted connection from:", address)

def extract_data(data):
    data = data.replace("b", "")
    data = data.replace("'", "")
    data = data.split(",")

    json_data = {'ir': data[0], 'x': data[1], 'y': data[2], 'z': data[3]}

    print(json_data)
    return json_data

topic = "world"

def on_publish(client, userdata, mid):
   print("published:" + str(mid))

def on_message(client, userdata, msg):
   print("msg:" + str(msg.payload.decode()))

def on_connect(client, userdata, flags, rc, topic):
    print("Connected with result code:" + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic)

# Can MQTT protocol and BT setup be done in parallel with threading?
    # Wait for both processes to be complete before proceeding?
    # Need to generate a certificate
# MQTT protocol setup
broker = "iot.eclipse.org"
mqtt_port = 1883

client = mqtt.Client()
client.on_publish = on_publish
client.on_message = on_message
client.on_connect = on_connect

X = client.connect(broker, port=mqtt_port)
print("Result:" + X)
time.sleep(0.025)

if X == 0:
    client.loop_start()
else:
    print("Pas de connexion")

while 1:
    data = client_sock.recv(1024)

    currentTime = datetime.datetime.now()
    print("Message received at:", currentTime)
    print("Data:", data)

    # print("Publishing to" + topic + "...")
    # client.publish(topic=topic, payload="msgMsg4GdLuck", qos=1)
    # print(mqtt.error_string(client.publish(topic="world", payload=b'msg', qos=1).rc))

# client.loop_stop()
# client.disconnect()
# server_sock.close()

