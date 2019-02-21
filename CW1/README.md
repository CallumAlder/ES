# An IoT MIDI Controller


[GitHub hosted webpage](https://callumalder.github.io/ES/)
- Select the 'App' in the navbar to go to the app page that hosts the main IOT interface.
- Webpage files can be found in the [docs folder](https://github.com/CallumAlder/ES/tree/master/docs)


## Installation

1. Setup the python environement 
    ````
    # Create a virtual environement for storing your stuf:
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

