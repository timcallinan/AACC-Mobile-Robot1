#!/bin/sh
# Test for gamepad and that it is in the correct mode, asking the driver to reset the receiver if necessary
# Then start the L4_control.py script to allow gamepad control and ball tracking if the LT button is pressed.

# Wait for the system to stabilize
sleep 60

DIR=/home/pi/SCUTTLE/trackball
cd ${DIR}

# Use lsusb for operation and cat usb.out for testing
CMD="lsusb"
#CMD="cat usb.out"

# Check that the gamepad receiver is in EMS-9101 mode
# Could enhance by stating what GP mode was detected
while !($CMD | grep "ESM-9101"); do
    echo "Looking for ESM-9101 mode"
    echo "The game pad is not in ESM 9 1 0 1 mode. Please unplug and replug the game pad receiver" | festival --tts
    sleep 10
done
TXT=" The Game pad is in the correct mode, you may now control the robot with the game pad"
echo $TXT
echo $TXT | festival --tts
echo "Start L4_command.py"
# Important! The virtual environment version of python must be started!
# This is instead of trying to source the virtual environment.
/home/pi/venv/bin/python3 ./L4_control.py

