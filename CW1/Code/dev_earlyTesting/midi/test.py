import mido
import pigpio

pi1 = pigpio.pi()
outport = mido.open_output('f_midi')  # open USB port

onmess = mido.Message('note_on', note = 34, velocity = 127)
offmess = mido.Message('note_off', note = 34, velocity = 127)

buttPin = 21
pi1.set_mode(buttPin, pigpio.INPUT)


def buttonDown(gpio, level, tick):
    print("DOWN")
    #outport.send(onmess)


def buttonUp(gpio, level, tick):
    print("UP")
    #outport.send(offmess)


cb = pi1.callback(buttPin, pigpio.RISING_EDGE, buttonDown)
cb2 = pi1.callback(buttPin, pigpio.FALLING_EDGE, buttonUp)
# Just loop and do nothing
while True:
    pass
