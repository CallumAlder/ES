import bluetooth
import datetime

import paho.mqtt.client as mqtt
import time

# BT setup
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
# bt_port = 1
server_sock.bind(("", 1))

# Server listens to accept one connection at a time
server_sock.listen(1)

# server_sock.accept() is a blocking call
client_sock, address = server_sock.accept()
print("Accepted connection from:", address)

# TODO: Have this assigned by a pipe? Rather than a global variable
broker_msg = ""

def extract_data(s_data):
    s_data = s_data.replace("b", "")
    s_data = s_data.replace("'", "")
    s_data = s_data.split(",")

    json_data = {"prx": s_data[0], "xGy": s_data[1], "yGy": s_data[2], "zGy": s_data[3]}

    print("JSON Data:", json_data)
    return json_data

# Specify topic to subscribe and publish to
publish_topic1 = "IC.embedded/skadoosh/sensor"
listen_topic1 = "IC.embedded/skadoosh/midi"

def on_publish(client, userdata, mid):
   print("published:" + str(mid))

def on_message(client, userdata, msg):
    get_mqtt_msg(msg)

def get_mqtt_msg(msg):
    msg = str(msg.payload.decode())
    print("msg: " + msg)
    # return

def on_connect(client, userdata, flags, rc, topic):
    print("Connected with result code:" + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(listen_topic1)
    client.subscribe(publish_topic1)

# TODO - MQTT
# Can MQTT protocol and BT setup be done in parallel with threading?
    # Wait for both processes to be complete before proceeding?
    # Need to generate a certificate
# MQTT protocol setup
broker = "iot.eclipse.org"
mqtt_port = 1883

client = mqtt.Client()
# client.on_publish = on_publish
client.on_message = on_message
client.on_connect = on_connect

X = client.connect(broker, port=mqtt_port)
print("Client Connection Result:")
print(X)
time.sleep(0.025)

if X == 0:
    client.loop_start()
else:
    print("Pas de connexion")

while 1:
    data = str(client_sock.recv(1024))

    currentTime = datetime.datetime.now()
    print("Message received at:", currentTime)
    j_data = extract_data(data)

    # print("Publishing to" + topic + "...")
    # print(mqtt.error_string(client.publish(topic=publish_topic1, payload=json.dumps(j_data), qos=1).rc))
    client.publish(topic=publish_topic1, payload=json.dumps(j_data), qos=1)

# client.loop_stop()
# client.disconnect()
# server_sock.close()

