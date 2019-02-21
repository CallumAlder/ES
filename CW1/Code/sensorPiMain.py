import time
import datetime
import json
import paho.mqtt.client as mqtt
import sensorPiClass
import ErrorHandling

from time import sleep
from math import log

spi = sensorPiClass.SenPi(pi="senPi")
spi.init_light()
spi.init_acc()


# Callbacks for events occurring with the MQTT broker
def on_publish(client, userdata, mid):
    print("Published: " + str(mid))


def on_message(client, userdata, msg):
    msg = str(msg.payload.decode())
    print("Received: " + msg)

    if msg == "map@chg":
        print("Turn change LED on...")
        spi.flash_led(spi.CHANGE_LED, 2)

MQTT_CONNECTED = False
def on_connect(client, userdata, flags, rc):
    # The client has connected to the broker
    print("Connected with result code: " + str(rc))
    global MQTT_CONNECTED
    MQTT_CONNECTED = True
    # This Pi will be listening to messages on this topic
    client.subscribe()

    # Provides user feedback (green light)
    spi.flash_led(spi.SUCCESS_LED, 2)


def on_disconnect():
    global MQTT_CONNECTED
    MQTT_CONNECTED = False

    # Attempt to reconnect
    connect_count = 0
    connect_broker = "iot.eclipse.org"
    connect_port = 8883

    # TODO: Broker Connection Error
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


def extract_data(s_data):
    s_data = s_data.replace("b", "")
    s_data = s_data.replace("'", "")
    s_data = s_data.split(",")

    json_data = {"prx": s_data[0], "xGy": s_data[1], "yGy": s_data[2], "zGy": s_data[3]}
    print("JSON Data:", json_data)
    return json_data


current_ir = 0
current_x = 0
current_y = 0
current_z = 0

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
    # TODO: Broker Connection Error
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
            raise ErrorHandling.BrokerConnectionError
    except ErrorHandling.BrokerConnectionError:

        quit()

spi.flash_led(spi.SUCCESS_LED, 2)

# Get range of data values for all sensors
max_array, min_array, med_array = spi.sensor_calibration()
print("Parameters for calibration extracted.")


while True:
    if MQTT_CONNECTED:
        # Handling IR sensor data for dynamic proximity approximation
        ir = spi.ir_weight * 1.47 * log(spi.lightSensor.readIR())
        max_array[0], min_array[0], update_med = spi.min_max_test(raw=ir, max=max_array[0],
                                                                  min=min_array[0], med_bool=1)
        if update_med:
            med_array[0] = (max_array[0] + min_array[0]) / 2
        current_ir, print_ir = spi.update_sensor_out(curr=current_ir, val=ir, max_val=max_array[0],
                                                     med_val=med_array[0], min_val=min_array[0],
                                                     weight=spi.ir_weight, threshold=8)

        # Handling gyroscope data
        x = spi.agSensor.getX()
        max_array[1], min_array[1], update_med = spi.min_max_test(raw=x, max=max_array[1],
                                                                  min=min_array[1], med_bool=1)
        if update_med:
            med_array[1] = (max_array[1] + min_array[1]) / 2
        current_x, print_x = spi.update_sensor_out(curr=current_x, val=x, max_val=max_array[1],
                                                   med_val=med_array[1], min_val=min_array[1],
                                                   weight=spi.x_weight, threshold=17)

        y = spi.agSensor.getY()
        max_array[2], min_array[2], update_med = spi.min_max_test(raw=y, max=max_array[2],
                                                                  min=min_array[2], med_bool=1)
        if update_med:
            med_array[2] = (max_array[2] + min_array[2]) / 2
        current_y, print_y = spi.update_sensor_out(curr=current_y, val=y, max_val=max_array[2],
                                                   med_val=med_array[2], min_val=min_array[2],
                                                   weight=spi.y_weight, threshold=15)

        z = spi.agSensor.getZ()
        max_array[3], min_array[3], update_med = spi.min_max_test(raw=z, max=max_array[3],
                                                                  min=min_array[3], med_bool=1)
        if update_med:
            med_array[3] = (max_array[3] + min_array[3]) / 2
        current_z, print_z = spi.update_sensor_out(curr=current_z, val=z, max_val=max_array[3],
                                                   med_val=med_array[3], min_val=min_array[3],
                                                   weight=spi.z_weight, threshold=15)

        # Can probably format data (output from the function below) as a dict
        data = spi.to_send(print_ir, print_x, print_y, print_z)
        if data != "nan":
            currentTime = datetime.datetime.now()
            print("Message sent at:", currentTime)

            j_data = extract_data(data)
            print("Publishing to " + spi.publish_topic1 + "...")
            print(mqtt.error_string(client.publish(topic=spi.publish_topic1, payload=json.dumps(j_data), qos=1).rc))
        sleep(0.1)
    else:
        print("Pas de connexion")
        spi.flash_led(spi.FAIL_LED, 2)
        client.loop_stop()
        client.disconnect()
        break
