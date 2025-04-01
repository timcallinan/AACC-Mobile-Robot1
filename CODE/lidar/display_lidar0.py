import time
import math
import matplotlib.pyplot as plt
from rplidar import RPLidar

# Configure your RPLidar port here
PORT = '/dev/ttyUSB0'  # Change this based on your system

# Initialize the RPLidar
lidar = RPLidar(PORT)

# Function to handle lidar data and plot it
def plot_lidar_data():
    try:
        print("Starting LIDAR scan...")
        lidar.start_motor()
        
        # Collecting scan data
        for scan in lidar.iter_scans():
            angles = []
            distances = []

            # Extract the angle and distance from the scan
            for (_, angle, distance) in scan:
                if distance > 0:
                    angles.append(math.radians(angle))  # Convert degrees to radians
                    distances.append(distance)

            print("Plotting data")            
            # Plotting the data
            plt.clf()  # Clear the plot for each new frame
            plt.subplot(projection='polar')
            plt.scatter(angles, distances, s=10, c='red', alpha=0.5)
            plt.title('RPLidar A1M8 Scan')
            plt.draw()
            plt.pause(0.1)  # Small pause to update plot

    except KeyboardInterrupt:
        print("Stopping the lidar scan.")
    finally:
        lidar.stop_motor()
        lidar.stop()
        lidar.disconnect()
        plt.show()

if __name__ == '__main__':
    plt.ion()  # Turn on interactive mode for live updates
    plot_lidar_data()
