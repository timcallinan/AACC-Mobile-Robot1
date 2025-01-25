#!/usr/bin/env python3

"""
Ball Following Script for SCUTTLE Robot
Integrates standard SCUTTLE software libraries
"""

import numpy as np
import time
#import pygame
import cv2

# Import standard SCUTTLE modules
import L1_motor as motor
#import basics_pi.mpu_function as mpu
import L1_gamepad as gamepad

class SCUTTLEBallFollower:
    def __init__(self):
        # Initialize gamepad
        gamepad.init()
        
        # Camera setup
        self.cap = cv2.VideoCapture(0)
        
        # Ball tracking variables
        self.ball_tracking_active = False
        
        # Color range for orange ball (adjustable)
        self.lower_orange = np.array([5, 100, 100])
        self.upper_orange = np.array([20, 255, 255])
        
        # PID-like control parameters
        self.Kp = 0.005  # Proportional gain
        self.max_turn_speed = 0.5  # Maximum turn speed
        
        # Visualization settings
        self.show_visualization = True
    
    def detect_ball(self, frame):
        """
        Detect ball in the frame
        Returns dictionary with ball information or None
        """
        # Convert to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create mask for orange ball
        mask = cv2.inRange(hsv, self.lower_orange, self.upper_orange)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # If no contours, return None
        if not contours:
            return None
        
        # Find largest contour (ball)
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Calculate moment to find center
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            # Ball center coordinates
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            
            # Calculate ball radius using equivalent circle diameter
            area = cv2.contourArea(largest_contour)
            radius = int(np.sqrt(area / np.pi))
            
            # Visualize ball if enabled
            if self.show_visualization:
                frame = self.visualize_ball(frame, cx, cy, radius)
            
            return {
                'x': cx,
                'y': cy,
                'radius': radius,
                'frame': frame
            }
        
        return None
    
    def visualize_ball(self, frame, cx, cy, radius):
        """
        Draw center dot and circumference of the ball
        """
        # Draw center dot (small red dot)
        cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
        
        # Draw circumference (green circle)
        cv2.circle(frame, (cx, cy), radius, (0, 255, 0), 2)
        
        return frame
    
    def follow_ball(self, frame):
        """
        Calculate motor speeds to follow ball
        """
        # Get ball information
        ball_info = self.detect_ball(frame)
        
        if ball_info is not None:
            # Frame center
            frame_center = frame.shape[1] // 2
            
            # Calculate error (deviation from center)
            error = ball_info['x'] - frame_center
            
            # Proportional control
            turn_speed = error * self.Kp
            
            # Limit turn speed
            turn_speed = np.clip(turn_speed, -self.max_turn_speed, self.max_turn_speed)
            
            # Base forward speed
            forward_speed = 0.3  # Moderate forward movement
            
            # Calculate motor speeds
            left_speed = forward_speed - turn_speed
            right_speed = forward_speed + turn_speed
            
            # Set motor speeds
            motor.motor_fwd_kin(left_speed, right_speed)
            
            # Display frame with ball visualization if enabled
            if self.show_visualization:
                cv2.imshow('Ball Tracking', ball_info['frame'])
                cv2.waitKey(1)
            
            return True
        
        # Stop if no ball detected
        motor.motor_fwd_kin(0, 0)
        return False
    
def run(self):
    """
    Main control loop
    """
    try:
        # Optional window for visualization
        if self.show_visualization:
            cv2.namedWindow('Ball Tracking', cv2.WINDOW_NORMAL)
        
        while True:
            # Read gamepad inputs
            gamepad.read_log()
            
            # Check for ball following trigger (LT button)
            if gamepad.axes[2] > 0.5:
                # Capture frame
                ret, frame = self.cap.read()
                if ret:
                    # Attempt to follow ball
                    self.follow_ball(frame)
            else:
                # Stop motors when not tracking
                motor.motor_fwd_kin(0, 0)
                
                # Close visualization window if open
                cv2.destroyAllWindows()
            
            # Small delay
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("Keyboard interrupt. Stopping motors.")
    
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
    
    finally:
        # Always ensure motors are stopped and resources are cleaned up
        motor.motor_fwd_kin(0, 0)
        self.cap.release()
        cv2.destroyAllWindows()

# Main execution
if __name__ == "__main__":
    robot = SCUTTLEBallFollower()
    robot.run()
