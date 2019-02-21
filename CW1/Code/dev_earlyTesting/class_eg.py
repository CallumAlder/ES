from midi_class import MidiOUT
from time import sleep

Enzo = MidiOUT('enzo', 176, '/dev/ttyAMA0', baud=38400)

while 1:
    Enzo.send_data("DRY", 0)
    sleep(2)
    Enzo.send_data("MONO", 0)
    sleep(2)
    Enzo.send_data("ARP", 0)
    sleep(2)
    Enzo.send_data("POLY", 0)
    sleep(2)
