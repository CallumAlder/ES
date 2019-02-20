import paho.mqtt.client as mqtt
import json
import time

from CW1.Code.midi_class import MidiOUT
from CW1.Code.sensorPiClass import SenPi

synPi = SenPi(debug=True)
Enzo = MidiOUT('enzo', 176, '/dev/ttyAMA0', baud=38400)


def on_publish(client, userdata, mid):
    print("Published: " + str(mid))


def on_message(client, userdata, msg):
    msg_dict = msg.payload.decode()
    json_msg = json.loads(msg_dict)
    print("msg: " + str(msg_dict))
    print("json: ", json_msg)
    for key, value in json_msg.items():
        # Do enzo stuff for each element of json dict.
        enzo_comms(Enzo, key, value)
        print("Key: {0}, Value: {1}".format(key, value))


def enzo_comms(enzo, control, value):
    enzo.send_data(control, value)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))

    # Listen topic
    client.subscribe(synPi.listen_topic1)
    print("Subscribing to: " + synPi.listen_topic1 + "...")


broker = "iot.eclipse.org"
port = 1883

client = mqtt.Client()
client.on_publish = on_publish
client.on_message = on_message
client.on_connect = on_connect

client.tls_set(ca_certs="eclipse-cert.pem",
               certfile="client.crt",
               keyfile="client.key")

X = -1
start = time.time()
while X != 0:
    time.sleep(0.5)
    try:
        # Attempt to connect to the MQTT Broker
        X = client.connect(broker, port=port)
    except:     # Add an exception type to catch
        # Flash the red (FAIL) LED
        print("Error - RED LED on. X: " + str(X))
        synPi.flash_led(synPi.FAIL_LED, 2)

time.sleep(0.25)
client.loop_start()
while True:
    if X != 0:
        client.loop_stop()
        client.disconnect()
        print("Pas de connexion")
        break
    else:
        print("Waiting for data...")
