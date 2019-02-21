import bluetooth
import datetime
# import serial

# ser = serial.Serial(port="/dev/rfcomm0",
#                     baudrate=115200)

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
port = 1

# Server binds the script on host to port 3
uuid = "00001101-0000-1000-8000-00805F9B34FB"
# port = bluetooth.get_available_port(bluetooth.RFCOMM)
# print("Port:", port)
# server_sock.bind(("", port))

def timefn(x):
    tData = str(data).replace("'", "")
    tData = tData.split(":")
    currentTime = datetime.datetime.now()
    print("Received message at - ", currentTime)
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

server_sock.bind(("", port))

# Server listens to accept one connection at a time
server_sock.listen(1)

# Was previously unable to perform advertise_service correctly so changed one line in:
# sudo nano /etc/systemd/system/dbus-org.bluez.service
# from ExecStart = ExecStart=/usr/lib/bluetooth/bluetoothd
# to ExecStart = ExecStart=/usr/lib/bluetooth/bluetoothd -C
# which is supposedly some compatibility mode. Also use superPython
bluetooth.advertise_service(server_sock,
                            "piExchange",
                            service_id=uuid,
                            service_classes=[bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE])

# server_sock.accept() is a blocking call
client_sock, address = server_sock.accept()
print("Accepted connection from:", address)

while 1:
    data = client_sock.recv(1024)
    timefn(data)

    client_sock.send(str(datetime.datetime.now()))
    currentTime = datetime.datetime.now()
    print("Message sent at -", currentTime)

bluetooth.stop_advertising(server_sock)
# client_sock.close()
server_sock.close()

# import bluetooth
# import serial
#
# ser = serial.Serial('/dev/rfcomm0')
# print(ser.name)
# ser.write(b'hello')
# ser.close()
#
# host = ""
# # port = 8888
#
# s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
# s.bind((host, 3))
# s.listen(1)
#
# conn, addr = s.accept()
# print("conn:", addr)
#
# while True:
#     data = conn.recv(1024)
#     if not data:
#         break
#     s.send("Back at ya")





