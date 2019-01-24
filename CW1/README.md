# Adafruit TMP007

[Adafruit Product Page](https://learn.adafruit.com/adafruit-tmp007-sensor-breakout/downloads)

## Data Sheet 
- [Adafruit version](https://cdn-shop.adafruit.com/datasheets/tmp007.pdf) was last revised in 2014, [TI on WayBack Machine](https://web.archive.org/web/20170320205345/http://www.ti.com/product/tmp007) last revised in 2015.

## Circuit Python Docs
- [Docs](https://circuitpython.readthedocs.io/projects/tmp007/en/latest/) - have been cloned to the folder: 


## Science
2. Research the sensorThis part can take place in parallel with other parts until parts 5 and 6.
    1. **What does it do?** infrared based temperature sensor
    2. **What is the power supply voltage? Some of the modules have power supplies in addition to the sensor chip so look for the documentation for the module.** Optimally works at 3.3V but can work from 2.5V to 5.5V, draws 270 μA while running.
    3. **What is the control flow for the sensor?** Thermocouple based reading goes through an amplification stage. This is combined with a reference voltage and a local temperature reading and then dgitised in a 16-bit ADC. The Digitised sensor reading then goes to a Digital Control and Math Engine which reads from the EEPROM (that stores calibration coefficients) and then goes to a I²C and SMBUS interface.
        1. **Does it need enabling or configuring before use?** Yes from a code perspective.
        2. **Does it measure automatically or on demand?iii.How do you configure it (if applicable)?** Code allows on demand reading.
        3. **How do you request a measurement (if applicable)?** See Circuit Python example
        4.**How do you read back the result?** It comes in as a float so you can do whatever to read that.
        5. **What conversion is needed to convert the result into something meaningful?** Nothing really as it comes as relative to the circuit temperature already.