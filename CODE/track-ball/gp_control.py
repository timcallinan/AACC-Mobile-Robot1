#!/usr/bin/env python
# gp_control.py
# Control the Scuttle robot for ball tracking safety.

# Import External programs
import numpy as np
import time

# Import Internal Programs
import gamepad as gp
import L1_log as log
import L2_inverse_kinematics as inv
import L2_kinematics as kin
import L2_speed_control as sc

# Run the main loop
while True:
    
    # COLLECT GAMEPAD COMMANDS
    gp_data = gp.getGP()
    print("GP Data:", gp_data)
    axis0 = gp_data[0] * -1
    axis1 = gp_data[1] * -1
    rthumb = gp_data[3] # up/down axis of right thumb
#    horn = gp_data[4]   # "y" button
    
    phiDots = kin.getPdCurrent()
    myString = str(round(phiDots[0],1)) + "," + str(round(phiDots[1],1))
    log.stringTmpFile(myString,"phidots.txt")

    myString = str(round(axis0*100,1)) + "," + str(round(axis1*100,1))
    print("Gamepad, xd: " , str(round(axis0,2)), " td: ", str(round(axis1,2)), " Rounded: ", myString) # print gamepad percents
    for i in range(4,15):
        print(i, ":", int(gp_data[i]), ' ', end='')
    print("")
    
    # DRIVE IN OPEN LOOP
    chassisTargets = inv.map_speeds(np.array([axis1, axis0])) # generate xd, td
    pdTargets = inv.convert(chassisTargets) # pd means phi dot (rad/s)
    
    #DRIVING
    sc.driveOpenLoop(pdTargets) #call driving function 
    time.sleep(1.05)
