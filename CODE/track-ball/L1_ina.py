# This code is adapted from: github.com/chrisb2/pi_ina219 examples
# This basic code samples voltage and uses auto-ranging.
# WARNING: configure ina sensor for address 0x44. Encoder occupies 0x40.

import time                 # for keeping time
import ina219               # for reading voltage/current sensor
from ina219 import INA219   # sensor library

# Declare relevant variables
SHUNT_OHMS = .01 # Measure your shunt with a multimeter & update.

# Set up the INA219 sensor
ina = INA219(SHUNT_OHMS, address = 0x44, busnum=1)
ina.configure(ina.RANGE_16V)

def readall():
    try:
        print("Bus Voltage: %.3f V" % ina.voltage())
        print("Bus Current: %.3f mA" % ina.current())
        print("Power: %.3f mW" % ina.power())
        print("Shunt voltage: %.3f mV" % ina.shunt_voltage())
    except DeviceRangeError as e:
        # Current out of device range with specified shunt resistor
        print(e)

def readVolts():
    volts = ina.voltage()
    return volts

def readShunt():
    shunt = ina.shunt_voltage()
    return shunt

def readAmps():
    amps = ina.current() / 1000  # Convert from mA to A
    return amps

##################

if __name__ == "__main__":
    while True:
        volts = round(readVolts(),2)
        shunt = round(readShunt(),2)
        amps = round(readAmps(), 2)
        print("Buss:", volts, "V  ", amps, "A   Shunt:", shunt, "mv")
        time.sleep(1)                       # pause
