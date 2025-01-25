#!/usr/bin/env python
# battery-to-lcd
#
# Runs from cron every minute to check battery state and current draw.
# Output the voltage and current to the LCD with the backlight on.
# If the voltage is too low (<10.8v) or the current is too high (>3A),
# cause the LCD to blink several times to attract attention.
#
# TODO: output low voltage warning to the speaker
#
import L1_ina
import L1_lcd
import time

# Read from the INA219
volts = round(L1_ina.readVolts(),2)
shunt = round(L1_ina.readShunt(),2)
amps = round(L1_ina.readAmps(), 2)
print("Buss:", volts, "V  ", amps, "A   Shunt:", shunt, "mv")

# Write to the LCD and turn on the backlight.
L1_lcd.lcd.clear()
L1_lcd.lcd.backlight = True
txt = "{volts:.2f}V at {amps:.2f}A".format(volts=volts, amps=amps)
#print(txt)
L1_lcd.lcdMessage(txt)
# If voltage is less than 11, then blink the backlight
if (volts < 11):
    L1_lcd.lcd.backlight=False
    time.sleep(1)
    L1_lcd.lcd.backlight=True
    time.sleep(1)
    L1_lcd.lcd.backlight=False
    time.sleep(1)
    L1_lcd.lcd.backlight=True

