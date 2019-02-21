import paho.mqtt.client as mqtt
import json
import time
import midi_class
import sensorPiClass

synPi = sensorPiClass.SenPi(pi="synPi")
Enzo = midi_class.MidiOUT('enzo', 176, '/dev/ttyAMA0', baud=38400)


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


MQTT_CONNECTED = False
def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))

    global MQTT_CONNECTED
    MQTT_CONNECTED = True

    # Listen topic
    client.subscribe(synPi.listen_topic1)
    print("Subscribing to: " + synPi.listen_topic1 + "...")


def on_disconnect():
    print("Disconnected from broker")
    global MQTT_CONNECTED
    MQTT_CONNECTED = False

    # Attempt to reconnect
    connect_count = 0
    connect_broker = "iot.eclipse.org"
    connect_port = 8883
    while not MQTT_CONNECTED:
        try:
            # Attempt to connect to the MQTT Broker
            if connect_count == 1:
                client.connect_async(connect_broker, port=connect_port)
                client.loop_start()
                time.sleep(0.25)
            if not MQTT_CONNECTED:
                time.sleep(1)
            if connect_count >= 5:
                raise RuntimeError
        except RuntimeError:
            # Flash the red (FAIL) LED
            print("Connection to broker unsuccessful")
            spi.flash_led(spi.FAIL_LED, 2)
            quit()


broker = "iot.eclipse.org"
port = 8883

client = mqtt.Client()
client.on_publish = on_publish
client.on_message = on_message
client.on_connect = on_connect
client.on_disconnect = on_disconnect

# Client certificate details
client.tls_set(ca_certs="/home/pi/ES/CW1/Code/security_certs/")

connectCounter = 0
while not MQTT_CONNECTED:
    connectCounter += 1
    try:
        # Attempt to connect to the MQTT Broker
        if connectCounter == 1:
            client.connect_async(broker, port=port)
            client.loop_start()
            time.sleep(0.25)
        if not MQTT_CONNECTED:
            time.sleep(2)
        # client.loop_stop()
        if connectCounter >= 5:
            raise RuntimeError
    except RuntimeError:
        # Flash the red (FAIL) LED
        print("Connection to broker unsuccessful")
        spi.flash_led(spi.FAIL_LED, 2)
        quit()

while True:
    if MQTT_CONNECTED:
        # print("Waiting for data...")
        time.sleep(0.25)
    else:
        client.disconnect()
        print("Pas de connexion")
        break

    # time.sleep(0.25)
