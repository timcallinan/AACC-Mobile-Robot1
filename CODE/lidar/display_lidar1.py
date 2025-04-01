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

        # Set the radial limit for the plot
        RADIAL_LIMIT = 5000  # Set this to the maximum distance you want to display in the plot (in mm)

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
            ax = plt.subplot(projection='polar')

            # Scatter plot the lidar data
            ax.scatter(angles, distances, s=10, c='red', alpha=0.5)

            # Set the radial limit (distance range)
            ax.set_ylim(0, RADIAL_LIMIT)  # Set radial limits

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

