#!/usr/bin/env python3
# L4_control.py
# A control program to drive with gamepad and switch between track ball mode (Left Trigger on GP)
# and track tape mode (Right Trigger on GP). This provides a means for taking over control of the
# robot if it veers off track.
#
# TODO: Add line tracking
#       Improve termination cleanup
#       Show a camera view all the time, regardless of the mode (GamePad, Follow_ball, Follow_tape)
#          This change will likely require refactoring since the camera operations are burried
#          in L3_follow.py and its lower level functions.

# Import External programs
import numpy as np
import time
import os
import cv2

# Import Internal Programs
import L1_gamepad as gp
import L1_log as log
import L1_ina as batt
import L1_lcd
import L1_text2speech as tts
import L2_inverse_kinematics as inv
import L2_kinematics as kin
import L2_speed_control as sc
import L3_follow as ball
import sensorScript as lineSensor

# Run the main
t0 = time.time()
lcd_update_period = 5		# seconds
voltage_warning = 10.0
warning_max = 10
warning_count = warning_max
voltage_sample_count = 3
voltage_sample_list = []
voltage_sample_index = 0
# initialize voltage list history
for i in range(0, voltage_sample_count):
    voltage_sample_list.append(batt.readVolts())
#print(voltage_sample_list)

while True:

    # Update LCD with battery info every N seconds and check for low voltage warning
    # by checking the mean of N samples
    t1 = time.time()
    if (t1 - t0) > lcd_update_period:
        # Get voltage and current and Write to LCD and Store voltage in a list
        volts = batt.readVolts()
        amps = batt.readAmps()
        L1_lcd.lcd.clear()
        L1_lcd.lcd.backlight = True
        txt = "{volts:.2f}V at {amps:.2f}A".format(volts=volts, amps=amps)
        print(txt)
        L1_lcd.lcdMessage(txt)
        #print("index:", voltage_sample_index, "warning_count", warning_count)
        voltage_sample_list[voltage_sample_index] = volts
        # Increment list index, circularly
        voltage_sample_index += 1
        if (voltage_sample_index >= voltage_sample_count):
            voltage_sample_index = 0
        # If average of the list values is less than voltage_warning, speak up
        voltage_average = (sum(voltage_sample_list) / len(voltage_sample_list))
        #print("average:", voltage_average)
        if (warning_count == 0):
            warning_count = warning_max
            if (voltage_average < voltage_warning):
                tts.say("Warning, Warning, battery is getting low")
        warning_count -= 1
        t0 = t1

    # # ACCELEROMETER SECTION
    # accel = mpu.getAccel()                          # call the function from within L1_mpu.py
    # (xAccel) = accel[0]                             # x axis is stored in the first element
    # (yAccel) = accel[1]                             # y axis is stored in the second element
    # #print("x axis:", xAccel, "\t y axis:", yAccel)     # print the two values
    # axes = np.array([xAccel, yAccel])               # store just 2 axes in an array
    # log.NodeRed2(axes)                              # send the data to txt files for NodeRed to access.
    
    # COLLECT GAMEPAD COMMANDS
    gp_data = gp.getGP()
    #print("Y", gp_data[4], "B", gp_data[5], "A", gp_data[6], "X", gp_data[7], "LB", gp_data[8], "RB", gp_data[9], "LT", gp_data[10], "RT", gp_data[11])
    axis0 = gp_data[0] * -1
    axis1 = gp_data[1] * -1
    rthumb = gp_data[3] # up/down axis of right thumb
    say_greeting = gp_data[6]   	# "A" button
    say_battery = gp_data[5]		# "B" button
    enable_follow_ball = gp_data[10]	# Left Trigger
    enable_follow_tape = gp_data[11]	# Right Trigger
    
    if say_greeting:
        #print("speak button")
        tts.say("Hi, Mr. C., How are you doing today?")

    if say_battery:
        #print("bstate button")
        os.system("/home/pi/venv/bin/python3 ./battery-to-speaker.py > /dev/null")

    if enable_follow_ball:
        ball.follow_ball()

    elif enable_follow_tape:
        print("line tracking")
        lineSensor.trackLine()

    else:   # Default is GP manual control

        phiDots = kin.getPdCurrent()
        myString = str(round(phiDots[0],1)) + "," + str(round(phiDots[1],1))
        log.stringTmpFile(myString,"phidots.txt")
    
        myString = str(round(axis0*100,1)) + "," + str(round(axis1*100,1))
        log.stringTmpFile(myString,"uFile.txt")
        print("Gamepad, xd:", round(axis1,3), "td: ", round(axis0,3)) # print gamepad percents
        
        # DRIVE IN OPEN LOOP
        chassisTargets = inv.map_speeds(np.array([axis1, axis0])) # generate xd, td
        pdTargets = inv.convert(chassisTargets) # pd means phi dot (rad/s)
        # phiString = str(pdTargets[0]) + "," + str(pdTargets[1])
        # print("pdTargets (rad/s): \t" + phiString)
        # log.stringTmpFile(phiString,"pdTargets.txt")
        
        #DRIVING
        sc.driveOpenLoop(pdTargets) #call driving function 
        #servo.move1(rthumb) # control the servo for laser
    
    time.sleep(.05)
    # use pollKey to handle the event loop

    # NEED BETTER TERMINATION AND CLEANUP
    if cv2.pollKey() & 0XFF ==ord('q'):
        break
