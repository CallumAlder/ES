import time
import rtmidi
import serial
import argparse

# Make parser
parser = argparse.ArgumentParser(add_help=True)

# Get args
parser.add_argument('-d', '--debug', help='show midi message',
                    action='store_true') 

# Format args
args = parser.parse_args()

# Set MIDI port
midiin = rtmidi.MidiIn()
midiin.open_virtual_port("UART_MIDI_OUT")  # Virtual MIDI
ser = serial.Serial('/dev/ttyAMA0', baudrate=38400)  # Open serial at 38400bps
midiin.ignore_types(sysex=False, timing=True, active_sense=True)
timer = time.time()
while True:
      msg = midiin.get_message()
      if msg:
         message, deltatime = msg
         timer += deltatime
         if args.debug:
            print (message)
         else :
           pass
         outmidi = [chr(i) for i in message]
         ser.write(outmidi)
         continue
