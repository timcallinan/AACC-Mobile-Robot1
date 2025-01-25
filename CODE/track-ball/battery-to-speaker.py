#!/home/pi/venv/bin/python3
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
import L1_text2speech

# Read from the INA219
volts = round(L1_ina.readVolts(),2)
shunt = round(L1_ina.readShunt(),2)
amps = round(L1_ina.readAmps(), 2)
#print("Buss:", volts, "V  ", amps, "A   Shunt:", shunt, "mv")

# Send to speaker
txt = "Voltage is {volts:.1f} , at {amps:.2f} Amps".format(volts=volts, amps=amps)
print(txt)
L1_text2speech.say(txt)
