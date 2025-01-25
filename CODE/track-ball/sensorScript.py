#Import external libraries
from gpiozero import Button
import time
import L1_motor as motor
# from error_catching import OuterSensorError
 
# Setup GPIO pins
sensorLeft = Button(5, pull_up=False)
sensorCenter = Button(6, pull_up=False)
sensorRight = Button(13, pull_up=False)
 
def read_sensors():
    return int(sensorLeft.is_pressed)*4 + int(sensorCenter.is_pressed)*2 + int(sensorRight.is_pressed)
 
def control_motors(left_speed, right_speed):
    # Set motor speeds (you can modify these based on your motor driver)
    motor.sendLeft(left_speed)
    motor.sendRight(right_speed)
    pass

    
def determineMovement(key):
    #The following comments represent the reading from sensors

        if key == 0: #(0,0,0)
            control_motors(0.22,0.22)
            print("No black detected, Inching forward")
                
        elif key == 1: #(0,0,1)
            control_motors(0.3,0.1)
            print("right")
                
        elif key == 2: #(0,1,0)
            control_motors(0.5,0.5)
            print("straight")
                
        elif key == 4: #(1,0,0)

            control_motors(0.1,0.3)
            print("left")
                
        elif key == 3: #(1,1,0)
            control_motors(0,0.25)
            print("slight left")
        
        elif key == 6: #(0,1,1)
            control_motors(0.25,0)
            print("slight right")
    
        elif key == 7: #(1,1,1)
            control_motors(0,0)	
            print("stopped")
            
        elif key == 5: #(1,0,1)
            print("ERROR: detected Left and Right sensors at the same time")

def trackLine():
   key = read_sensors()
   print("key: ", key)
   determineMovement(key)

#testing function

if __name__ == "__main__":
   while True:
      trackLine() 
      time.sleep(0.2)

