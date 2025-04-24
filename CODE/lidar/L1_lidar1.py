# Import external libraries
import numpy as np                                  # for array handling
import time                                         # for timekeeping
import matplotlib.pyplot as plt                     # for plotting
from rplidar import RPLidar

# Initialize the lidar
lidar = RPLidar('/dev/ttyUSB0')

# Get and print lidar info
info = lidar.get_info()
print(info)

# Set numpy print options to suppress scientific notation
np.set_printoptions(suppress=True)                  # Suppress Scientific Notation

# Define the start angle for lidar points
start_angle = -135.0  # lidar points will range from -135 to 135 degrees

def polarScan(num_points=54):
    # Start collecting scans from the lidar
    scans = lidar.iter_scans()  # Start iterating over lidar scans

    # Collect only a single scan (you can collect multiple if you want)
    scan_data = next(scans)

    # LIDAR data properties
    dist_amnt = len(scan_data)  # Number of distance data points reported from the lidar
    angle_res = 360 / dist_amnt  # Angular resolution reported from lidar (assuming full 360 degree sweep)

    # Create the column of distances (scan data contains tuples of (quality, angle, distance))
    scan_points = np.array([data[2] for data in scan_data])  # Extract the distance values
    
    # Reshape scan_points to match num_points and handle in a way that avoids irregular shapes
    if dist_amnt < num_points:
        # If scan data contains fewer points than requested, repeat the data to match the required points
        scan_points = np.tile(scan_points, int(np.ceil(num_points / dist_amnt)))[:num_points]
    else:
        # If scan data contains more points, take evenly spaced samples
        indices = np.linspace(0, dist_amnt - 1, num_points, dtype=int)
        scan_points = scan_points[indices]

    # Create the column of angles
    angles = np.linspace(start_angle, start_angle + 360, num_points, endpoint=False)
    
    # Create the polar coordinates of scan
    scan_points = np.column_stack((scan_points, angles))  # Combine distances and angles

    # Round each element in array to 3 decimal places
    scan_points = np.round(scan_points, 3)

    return scan_points

def plot_lidar_data(scan_data):
    # Extract distances and angles from the scan data
    distances = scan_data[:, 0]
    angles = np.radians(scan_data[:, 1])  # Convert angles to radians for polar plotting

    # Plotting the data
    plt.clf()  # Clear the plot for each new frame
    ax = plt.subplot(projection='polar')

    # Scatter plot the lidar data
    ax.scatter(angles, distances, s=10, c='red', alpha=0.5)

    # Set radial limits (for example, 1000 mm)
    ax.set_ylim(0, 1000)

    # Set the direction of the angles (optional)
    ax.set_theta_direction(-1)  # Reverse angle direction if necessary

    # Set plot title
    plt.title('RPLidar A1M8 Scan')

    # Draw the plot
    plt.draw()
    plt.pause(0.1)  # Small pause to update plot

if __name__ == "__main__":
    # Enable interactive mode for live updates
    plt.ion()

    # Continuously get LIDAR data and plot
    while True:
        lidarData = polarScan(54)  # Collect LIDAR data
#        print(lidarData)  # Optionally print data for debugging
        plot_lidar_data(lidarData)  # Plot the LIDAR data
        time.sleep(1)  # Wait for 1 second before next scan

#    plt.show()  # Ensure the plot stays open after the loop ends

