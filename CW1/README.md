# SKAD00SH: An IoT MIDI Controller

The Skadoosh system is multi-sensory controller for any instrument synthesizer that 
uses MIDI communication. The current prototype works uses a proximity sensor and a 
3-axis gyroscope as inputs to control selected synthesizer outputs as decided 
on the Skadoosh [GitHub hosted webpage](https://callumalder.github.io/ES/)
- Select the 'App' in the navbar to go to the app page that hosts the main IOT interface, or go [here](https://callumalder.github.io/ES/app.html).
- Webpage files can be found in the [docs folder](https://github.com/CallumAlder/ES/tree/v1.0-beta/docs)

## Video Demo 
For the video demonstration of the system, you can download the video [here](https://github.com/CallumAlder/ES/blob/v1.0-beta/docs/vids/Skadoosh-Demo.mp4) or see it [hosted here](https://callumalder.github.io/ES/#videoDemo)!


## About the System
Skadoosh systems consists of two raspberry Pi micro-controllers. One Pi gathers sensor 
data and compresses each value to an output of 0 to 127 for the synthesizer to interpret 
an effect. This part of the system is the _sensor module_. The compressed values are 
communicated to the other Pi via an encrypted port of the public MQTT Broker: '[iot.eclipse.org](iot.eclipse.org)'. The other Pi is 
connected to the synthesizer via its serial port and communicates the mapped sensor data
to produce changes. This part of the system is the _MIDI module_. 

## Using the System 
1. Attach the sensor module to the instrument of your choosing in a way that is most 
comfortable
2. Connect the MIDI module to the synthesizer
3. Enjoy your enhanced sound!

## Code 
Please click here for the main code running in the modules: 
- [sensorPiMain.py](https://github.com/CallumAlder/ES/tree/v1.0-beta/CW1/Code/sensorPiMain.py) : runs on the sensor module, attached to your instrument.
- [synthPi.py](https://github.com/CallumAlder/ES/tree/v1.0-beta/CW1/Code/synthPi.py) : runs on the MIDI module.


## Installation
If you are interested in playing with the code yourself:
1. Setup the python environement 
    ````
    # Create a virtual environement for storing your stuff:
    # install venv (virtual environment)
    sudo apt-get install python3-venv
    # Create venv called skadoosh - it is stored in a folder in the current working directory
    python3 -m venv skadoosh
    
    # ACTIVATE YOUR ENVIRONMENT
    source skadoosh/bin/activate
    
    # ONLY RUN THE BELOW ONCE YOU HAVE ACTIVATED YOUR ENVIRONEMNT
    
    
    # NOTE: we do not use 'sudo' here as that would install these globally, instead of for this environement
    # GPIO Libraries
    pip3 install pigpio RPI.GPIO 
    # Install Adafruit GPIO libraries (offers some convenient functions)
    pip3 install Adafruit-GPIO
    # Install Serial Libraries
    pip3 install pyserial
    # Install numpy
    pip3 install libatlas-base-dev numpy
    # Install MQTT related
    pip3 install paho-mqtt
    ````
2. We need to apply a hack to the `paho-mqtt` implementation to allow us to pass a folder for security certificates instead of just a single file.
    ````
    # Change Line 772 of the mqtt client.py file
    nano +772 /home/pi/<user>/lib/python3.5/site-packages/paho/mqtt/client.py 
    # We want the following line instead:
    context.load_verify_locations(capath=ca_certs)
    ````

## Helpful Notes:

1. Scripts can be made 'executable' with a shebang, e.g: `#!/usr/bin/env python3`
Then using the terminal command: `chmod +x si1145.py` . Running the script can
then be done with: `./si1145.py`

