# Embdedded Systems - Skadoosh

# Skadoosh
The Skadoosh system is multi-sensory controller for any instrument synthesizer that 
uses MIDI communication. The current prototype works uses a proximity sensor and a 
3-dimensional gyroscope as inputs to control selected synthesizer outputs as decided 
on the Skadoosh website here.

# Video Demo 
For the video demonstration of the system, please see the video here!

# About the System
Skadoosh systems consists of two raspberry Pi micro-controllers. One Pi gathers sensor 
data and compresses each value to an output of 0 to 127 for the synthesizer to interpret 
and effect. This part of the system is the sensor module. The compressed values are 
communicated to the other Pi via an MQTT Broker: 'iot.eclipse.org'. The other Pi is 
connected to the synthesizer via its serial port and communicates the mapped sensor data
to produce changes. This part of the system is the MIDI module. 

# Using the System
1. Attach the sensor module to the instrument of your choosing in a way that is most 
comfortable
2. Connect the MIDI module to the synthesizer
3. Enjoy your enhanced sound!

# Code 
Please click here for the main code running in the modules: 

	- sensorPiMain.py
	- synthPi.py

# Notes
1. Run on Boot: Scripts can be made 'executable' with a shebang, 
e.g: #!/usr/bin/env python3. Then using the terminal command: chmod +x si1145.py 
running the script can then be done with: ./si1145.py.

2. Adding multiple certificates: /home/pi/<user>/lib/python3.5/site-packages/paho/mqtt/client.py 
Line 772 context.load_verify_locations(capath=ca_certs)
