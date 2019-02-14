import paho.mqtt.client as mqtt
import json
import time

def on_publish(client, userdata, mid):
   print("mid: " + str(mid))

def on_message(client, userdata, msg):
    msg_dict = msg.payload.decode()
    json_msg = json.loads(msg_dict)
    print("msg: " + str(msg_dict))
    print("json: ", json_msg)
    for key, value in json_msg.items():
        # Do enzo stuff for each element of json dict.
        print("Key: {0}, Value: {1}".format(key, value))

def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))

    # Listen topic
    listen_topic1 = "IC.embedded/skadoosh/midi"
    client.subscribe(listen_topic1)
    print("Subscribing to: " + listen_topic1 + "...")
    # Publish topic - it is not publishing anything?
    # client.subscribe("")

broker = "iot.eclipse.org"
port = 1883

client = mqtt.Client()
client.on_publish = on_publish
client.on_message = on_message
client.on_connect = on_connect

X = client.connect(broker, port=port)
print(X)

time.sleep(0.25)
if X == 0:
    print("Waiting for data...")
    client.loop_start()
    while 1:
        # time.sleep(0.1)

        # print("Publishing...")
        # client.publish(topic="world", payload="msgMsg4GdLuck", qos=1)
        # client.publish(topic="IC.embedded/skadoosh/midi", payload="msgMsg4GdLuck", qos=1)
        time.sleep(0.1)

        # print(mqtt.error_string(client.publish(topic="world", payload=b'msg', qos=1).rc))
        # client.loop_stop()
        # client.disconnect()
else:
    client.loop_stop()
    client.disconnect()
    print("Pas de connexion")
