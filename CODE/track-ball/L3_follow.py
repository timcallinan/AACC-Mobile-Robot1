# This is a demo for following a colored object.
# A basketball is an easy object to tune for colors and perform following
# Last updated 2021.06 DPM

# Import external programs
import time         # keeping time
import numpy as np  # for handling matrices
import cv2

# Import internal programs
import L2_track_target as track
import L2_speed_control as sc
import L2_inverse_kinematics as inv

# Declare relevant variables
radius = 0                          # radius of target
cruiseRate = 0.6                    # speed for cruising (fraction)
turnRate   = 0.8                    # speed for turning (fraction)
r1 = 40                             # radius desired (pixels)
tol = 5                             # radius tolerance (pixels)
centerBand = 0.20                   # portion of FOV to consider target centered

# Declare variables for time-keeping
#t1 = time.monotonic()  # declare vars
#t0 = t1              # for keeping time
#print("initial time: ", t1)

def forwardFunction(r0):            # when the target is straight on, approach          
    xdt = 0                         # initial x_dot target is zero
    if r0 < (r1 - tol):             # if target looks too small
        xdt = cruiseRate            # x_dot target, drive fwd       
        #print("Forward: target too small, r0, r1, tol:", r0, r1, tol)
    elif r0 > (r1 + tol):           # if target looks too big
        xdt = -1* cruiseRate        # x_dot target, drive backwards
        #print("Forward: target too large, r0, r1, tol:", r0, r1, tol)
    return xdt

def turnAndGo(x_offset, radius):                               # turn towards object and approach
    if abs(x_offset) > centerBand:                             # if x_offset is outside the band, make a turn
        pdt = np.sign(x_offset) * x_offset * x_offset * turnRate # square the offset, keep the sign, & scale by constant
        chassisTargets = inv.map_speeds(np.array([0, pdt]))    # generate xd, td
        #print("turnAndGo: turn", x_offset, pdt)
    else: 
        xdt = forwardFunction(radius)                          # determine forward speed
        chassisTargets = inv.map_speeds(np.array([xdt,0]))     # set td zero
        #print("turnAndGo: straight", radius)
    return chassisTargets

def follow_ball():
    target = track.colorTarget(track.color_range)           # generate a target
#    t1 = time.monotonic()                                   # measure loop end time
#    t = round(t1 - t0, 3)                                   # compute loop in seconds
#    t0 = t1                                                 # reset loop base

    if target[0] is None:                                   # if there is no colored target detected
        print("\tno target located.")			      # do not drive
        # Stop motors
        #openLoop(0,0)

    else:
        x_offset = round(track.getAngle(target[0]),2)       # find angle of the target's x_offset (% of FOV)
        radius = int(target[2])                             # find out the radius of the target
        chassisTargets = turnAndGo(x_offset, radius)        # take the x target location & generate turning
        pdTargets = inv.convert(chassisTargets)             # phi dot targets (rad/s)
        print("Follow Ball - Target x_offset: ", x_offset, "\t radius", radius, "pdTargets:", pdTargets)
        sc.driveOpenLoop(pdTargets)                         # command motors in open-loop fashion

# THIS SECTION ONLY RUNS IF THE PROGRAM IS CALLED DIRECTLY
if __name__ == "__main__":
    
    while True:
        follow_ball()
        if cv2.pollKey() & 0XFF ==ord('q'):
            break
