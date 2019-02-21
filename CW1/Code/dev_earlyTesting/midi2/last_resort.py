import time
import rtmidi

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

for port_name in available_ports:
    print(port_name)

#if available_ports:
#    print("in sad")
#    midiout.open_port(0)
#else:
print("here we go")
midiout.open_virtual_port("UART_MIDI_OUT")

note_on = [0x99, 60, 112] # channel 10, middle C, velocity 112
note_off = [0x89, 60, 0]
midiout.send_message(note_on)
time.sleep(0.5)
midiout.send_message(note_off)

del midiout
