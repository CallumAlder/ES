# Components 
## Adafruit TMP007

[Adafruit Product Page](https://learn.adafruit.com/adafruit-tmp007-sensor-breakout/downloads)

### Data Sheet 
- [Adafruit version](https://cdn-shop.adafruit.com/datasheets/tmp007.pdf) was last revised in 2014, [TI on WayBack Machine](https://web.archive.org/web/20170320205345/http://www.ti.com/product/tmp007) last revised in 2015.

### Circuit Python Docs
- [Docs](https://circuitpython.readthedocs.io/projects/tmp007/en/latest/) - have been cloned to the folder:
- But just pip install  


### Science
2. Research the sensorThis part can take place in parallel with other parts until parts 5 and 6.
    1. **What does it do?** infrared based temperature sensor
    2. **What is the power supply voltage? Some of the modules have power supplies in addition to the sensor chip so look for the documentation for the module.** Optimally works at 3.3V but can work from 2.5V to 5.5V, draws 270 μA while running.
    3. **What is the control flow for the sensor?** Thermocouple based reading goes through an amplification stage. This is combined with a reference voltage and a local temperature reading and then dgitised in a 16-bit ADC. The Digitised sensor reading then goes to a Digital Control and Math Engine which reads from the EEPROM (that stores calibration coefficients) and then goes to a I²C and SMBUS interface.
        1. **Does it need enabling or configuring before use?** Yes from a code perspective.
        2. **Does it measure automatically or on demand?iii.How do you configure it (if applicable)?** Code allows on demand reading.
        3. **How do you request a measurement (if applicable)?** See Circuit Python example
        4.**How do you read back the result?** It comes in as a float so you can do whatever to read that.
        5. **What conversion is needed to convert the result into something meaningful?** Nothing really as it comes as relative to the circuit temperature already.
        
        
## Adafruit 3-Axis Gyrometer + Accelerometer

[Adafruit Product Page](https://learn.adafruit.com/adafruit-lis3dh-triple-axis-accelerometer-breakout/downloads)

### Data Sheet / Resources
- [Adafruit version](https://cdn-shop.adafruit.com/datasheets/LIS3DH.pdf) was last revised in 2010, [ST](https://www.st.com/en/mems-and-sensors/lis3dh.html) last revised in 2016.
- AppNote's also exist detailing pins, calibration - ST is more updated.

### Circuit Python Docs
- [Docs](https://learn.adafruit.com/adafruit-lis3dh-triple-axis-accelerometer-breakout/python-circuitpython) - have been cloned to the folder: 
- but just pip install


### Science
 <!---
2. Research the sensorThis part can take place in parallel with other parts until parts 5 and 6.
    1. **What does it do?** infrared based temperature sensor
    2. **What is the power supply voltage? Some of the modules have power supplies in addition to the sensor chip so look for the documentation for the module.** Optimally works at 3.3V but can work from 2.5V to 5.5V, draws 270 μA while running.
    3. **What is the control flow for the sensor?** Thermocouple based reading goes through an amplification stage. This is combined with a reference voltage and a local temperature reading and then dgitised in a 16-bit ADC. The Digitised sensor reading then goes to a Digital Control and Math Engine which reads from the EEPROM (that stores calibration coefficients) and then goes to a I²C and SMBUS interface.
        1. **Does it need enabling or configuring before use?** Yes from a code perspective.
        2. **Does it measure automatically or on demand?iii.How do you configure it (if applicable)?** Code allows on demand reading.
        3. **How do you request a measurement (if applicable)?** See Circuit Python example
        4.**How do you read back the result?** It comes in as a float so you can do whatever to read that.
        5. **What conversion is needed to convert the result into something meaningful?** Nothing really as it comes as relative to the circuit temperature already.
--->
        
## Adafruit UV/IR Visible Sensor

[Adafruit Product Page](https://learn.adafruit.com/adafruit-si1145-breakout-board-uv-ir-visible-sensor/downloads)

### Data Sheet / Resources
- [Adafruit version](https://cdn-shop.adafruit.com/datasheets/LIS3DH.pdf) was last revised in 2013, [SiLabs](https://www.silabs.com/documents/public/data-sheets/Si1145-46-47.pdf) last revised in 2014.

### Circuit Python Docs
- NONE
- Python Library made here [Python Library](https://github.com/THP-JOE/Python_SI1145/blob/master/SI1145/SI1145.py) - have been cloned to the folder: 


### Science
 <!---
2. Research the sensorThis part can take place in parallel with other parts until parts 5 and 6.
    1. **What does it do?** infrared based temperature sensor
    2. **What is the power supply voltage? Some of the modules have power supplies in addition to the sensor chip so look for the documentation for the module.** Optimally works at 3.3V but can work from 2.5V to 5.5V, draws 270 μA while running.
    3. **What is the control flow for the sensor?** Thermocouple based reading goes through an amplification stage. This is combined with a reference voltage and a local temperature reading and then dgitised in a 16-bit ADC. The Digitised sensor reading then goes to a Digital Control and Math Engine which reads from the EEPROM (that stores calibration coefficients) and then goes to a I²C and SMBUS interface.
        1. **Does it need enabling or configuring before use?** Yes from a code perspective.
        2. **Does it measure automatically or on demand?iii.How do you configure it (if applicable)?** Code allows on demand reading.
        3. **How do you request a measurement (if applicable)?** See Circuit Python example
        4.**How do you read back the result?** It comes in as a float so you can do whatever to read that.
        5. **What conversion is needed to convert the result into something meaningful?** Nothing really as it comes as relative to the circuit temperature already.
--->
 ## Adafruit Bluetooth Module (BlueFruit)
 
 [Adafruit Product Page](https://learn.adafruit.com/introducing-the-adafruit-bluefruit-le-uart-friend/downloads)
 
 ### Data Sheet / Resources
 - [Adafruit version](https://cdn-shop.adafruit.com/datasheets/LIS3DH.pdf) was last revised in 2013, [SI](https://www.silabs.com/documents/public/data-sheets/Si1145-46-47.pdf) last revised in 2014.

 
 ### Circuit Python Docs
 - NONE
 - Python Library made here [Python Library](https://learn.adafruit.com/introducing-the-adafruit-bluefruit-le-uart-friend/software) - have been cloned to the folder: 
 
 
 ### Science
 <!---
 2. Research the sensorThis part can take place in parallel with other parts until parts 5 and 6.
     1. **What does it do?** infrared based temperature sensor
     2. **What is the power supply voltage? Some of the modules have power supplies in addition to the sensor chip so look for the documentation for the module.** Optimally works at 3.3V but can work from 2.5V to 5.5V, draws 270 μA while running.
     3. **What is the control flow for the sensor?** Thermocouple based reading goes through an amplification stage. This is combined with a reference voltage and a local temperature reading and then dgitised in a 16-bit ADC. The Digitised sensor reading then goes to a Digital Control and Math Engine which reads from the EEPROM (that stores calibration coefficients) and then goes to a I²C and SMBUS interface.
         1. **Does it need enabling or configuring before use?** Yes from a code perspective.
         2. **Does it measure automatically or on demand?iii.How do you configure it (if applicable)?** Code allows on demand reading.
         3. **How do you request a measurement (if applicable)?** See Circuit Python example
         4.**How do you read back the result?** It comes in as a float so you can do whatever to read that.
         5. **What conversion is needed to convert the result into something meaningful?** Nothing really as it comes as relative to the circuit temperature already.     
 --->  
 ## Installation


````
# Create a virtual environement for storing your stuf:
# install venv
sudo apt-get install python3-venv
# Create venv called skadoosh - it is stored in a folder in the current working directory
python3 -m venv skadoosh

# ACTIVATE YOUR ENVIRONMENT
source skadoosh/bin/activate

# ONLY RUN THE BELOW ONCE YOU HAVE ACTIVATED YOUR ENVIRONEMNT


# Install Circuit Python (Adafruit blinka)
# NOTE: we do not use 'sudo' here as that would install these globally, instead of for this environement
pip3 install RPI.GPIO
pip3 install adafruit-blinka
# Install Temperature sensor API (that uses Circuit-Python)
pip3 install adafruit-circuitpython-tmp007
# Install 3-Axis Gyro API (that uses Circuit-Python)
sudo pip3 install adafruit-circuitpython-lis3dh
# Install UV/IR Sensor [N/A via pip]
#
````