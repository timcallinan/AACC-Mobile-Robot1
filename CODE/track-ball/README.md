# Scuttle robot software for AACC robot 1


## Control functions

The robot software from the SCUTTLE repo worked for gamepad control without modification,
based on a copy of SCUTTLE/software/python/basics_pi directory.

We needed a way to control the robot while working on the line tracking and colored ball tracking
software so that if the robot went astray we could quickly regain control.

The line tracking software was integrated with the gamepad control system. The gamepad left-trigger (LT)
was used to enable line tracking when pressed. Releasing the LT button resumed gamepad control.

The RT (Right-Trigger) button was used to enable openCV ball tracking code.

## TODO
- Enhance line tracking code to search for a line and to handle the case of no sensors triggered or all three
sensors triggered.

- Add PID control algorithm to replace open-loop control.





