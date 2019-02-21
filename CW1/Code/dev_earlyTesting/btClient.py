import bluetooth
# import sys
import datetime
# import serial

# Client side raspberry pi

# ser = serial.Serial(port="/dev/rfcomm0",
#                     baudrate=115200)

def timefn(x):
    tData = str(data).replace("'", "")
    tData = tData.split(":")
    currentTime = datetime.datetime.now()
    print("Received message at -", currentTime)
    print(tData[1:])

    t2Data = str(currentTime).replace("'", "")
    t2Data = t2Data.split(":")
    print(t2Data[1:])

    if tData[1] != t2Data[1]:
        # timeTaken = (float(t2Data[1]) - float(tData[1])) + (float(t2Data[2]) - float(tData[2]))/100.0
        print(
        "Time Taken: ", (float(t2Data[1]) - float(tData[1])), "Minutes and ", (float(t2Data[2]) - float(tData[2])),
        "Seconds")
    else:
        print("Time Taken:", (float(t2Data[2]) - float(tData[2])), "Seconds")
        # timeTaken = (float(t2Data[2]) - float(tData[2]))
        # print(timeTaken)

uuid = "00001101-0000-1000-8000-00805F9B34FB"
target_name = "skad00shpi2"

bd_addr = "B8:27:EB:BF:51:05"

port = 1
client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
client_socket.connect((bd_addr, port))

while 1:
    client_socket.send(str(datetime.datetime.now()))
    currentTime = datetime.datetime.now()
    print("Message sent at -", currentTime)

    data = client_socket.recv(1024)
    timefn(data)

# client_socket.close()


# client_socket = BluetoothSocket(bluetooth.RFCOMM)
# client_socket.connect((host, port))
# client_socket.send("Suck your mum")
# client_socket.close()
# break

# import sys
# import bluetooth
# import serial
#
# ser = serial.Serial('/dev/rfcomm0')
# print(ser.name)
#
# ser.write(b'hello')
# ser.close()
#
# # host = sys.argv[1]
# # port = 8888
# target_addr = "b8:27:eb:40:ae:fa" # - server
# # B8:27:EB:BF:51:05 - own address - client
#
# client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
# client_sock.connect((target_addr, 3))
#
# message = "gimme the loot"
# client_sock.send(message)
# print("Message delivered")
#
# data = client_sock.recv(1024)
# print("Received:", data)
# client_sock.close()

# target_addr = "b8:27:eb:40:ae:fa"

# service_matches = []

# nearby_devices = bluetooth.discover_devices()
#
# for bdaddr in nearby_devices:
#     if target_addr == bdaddr:
#         break
#
# if target_addr is not None:
#     print("found target bt device: ", target_addr)
# else:
#     print("could not find device")
#
# services = bluetooth.find_service(uuid=uuid)
# print(services)
#
# for i in range(len(services)):
#     if services[i]["name"] == "piExchange":
#         port = services[i]["port"]
#         host = services[i]["host"]
#
#         print("Name: {%s}, Port: {%s}, Host: {%s}".format(services[i]["name"],
#                                                           port,
#                                                           host))










