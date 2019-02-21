import serial
import ErrorHandling

from time import sleep


# All the writeable values in this document were found, parsed and decoded from proprietary binary manually
# See

class MidiOUT:

    #  mess_chan=176, port='/dev/ttyAMA0', baud=38400
    def __init__(self, name, mess_chan, port, baud):

        self.__ser = serial.Serial(port, baudrate=baud, write_timeout=0)

        self.__name = name
        self.__mess_chan = mess_chan

        sleep(0.001)

        if not self.get_ser().isOpen():
            raise IOError("Failed to open serial port")

    def get_ser(self):
        return self.__ser

    def get_name(self):
        return self.__name

    def get_mess_chan(self):
        return self.__mess_chan

    def set_name(self, new_name):
        self.__name = new_name

    def set_mess_chan(self, new_mess_chan):
        self.__mess_chan = new_mess_chan

    def send_data(self, control, value):

        #  ---- STANDARD POTS ----
        if control == "PITCH":
            control = 16

        elif control == "FILTER":
            control = 17

        elif control == "MIX":
            control = 18

        elif control == "SUSTAIN":
            control = 19

        elif control == "ENVELOPE":
            control = 20

        elif control == "MODULATION":
            control = 21

        #  ---- ALTERNATE POTS ----
        elif control == "PORTAMENTO":
            control = 22

        elif control == "FILTERTYPE":
            control = 23

        elif control == "DELAYLEVEL":
            control = 24

        elif control == "RINGMODULATION":
            control = 25

        elif control == "FILTERBANDWIDTH":
            control = 26

        elif control == "DELAYFEEDBACK":
            control = 27

        #  ---- SYTNH MODE 4 WAY BUTTON ----
        elif control == "DRY":
            control = 29
            value = 31

        elif control == "MONO":
            control = 29
            value = 63

        elif control == "ARP":
            control = 29
            value = 95

        elif control == "POLY":
            control = 29
            value = 127

        #  ---- WAVESHAPE ----
        elif control == "SAWTOOTH":
            control = 30
            value = 63

        elif control == "MONO":
            control = 30
            value = 127

        else:
            return None

        try:
            enzo_write = self.__ser.write(bytearray([self.__mess_chan, control, value]))
            if enzo_write == 0:
                raise ErrorHandling.MIDIConnectionError
        except ErrorHandling.MIDIConnectionError:
            sleep(0.001)
        sleep(0.001)
