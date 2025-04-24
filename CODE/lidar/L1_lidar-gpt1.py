# This file performs the following:
# 1) Grab a subset of the readings from the lidar for lightweight purposes
# 2) Assign the proper angle value to the reading, with respect to the robot x-axis
# 3) Create a 2d array of [distances, angles] from the data

# Import external libraries
import numpy as np                                  # For array handling
import time                                         # For timekeeping
from rplidar import RPLidar                         # For RPLidar A1M8 interaction

# Initialize the lidar
lidar = RPLidar('/dev/ttyUSB0')                     # Change this port to match your setup

# Get and print lidar info
info = lidar.get_info()
print(info)

# Set numpy print options to suppress scientific notation
np.set_printoptions(suppress=True)                  # Suppress Scientific Notation

# Define the start angle for lidar points
start_angle = -135.0  # lidar points will range from -135 to 135 degrees

def polarScan(num_points=54):                       # You may request up to 811 points, max.
    # Start collecting scans from the lidar
    scans = lidar.iter_scans()  # Start iterating over lidar scans

    # Collect only a single scan (you can collect multiple if you want)
    scan_data = next(scans)

    # LIDAR data properties
    dist_amnt = len(scan_data)  # Number of distance data points reported from the lidar
    angle_res = 360 / dist_amnt  # Angular resolution reported from lidar (assuming full 360 degree sweep)

    # Create the column of distances (scan data contains tuples of (quality, angle, distance))
    scan_points = np.array([data[2] for data in scan_data])  # Extract the distance values

    # If the scan has more points than requested, sample evenly
    if dist_amnt > num_points:
        indices = np.linspace(0, dist_amnt - 1, num_points, dtype=int)  # Evenly spaced indices
        scan_points = scan_points[indices]  # Select the data points at those indices
    else:
        # If fewer data points than requested, repeat or trim to match num_points
        scan_points = np.tile(scan_points, int(np.ceil(num_points / dist_amnt)))[:num_points]

    # Create the column of angles
    angles = np.linspace(start_angle, start_angle + 360, num_points, endpoint=False)
    
    # Create the polar coordinates of scan
    scan_points = np.column_stack((scan_points, angles))  # Combine distances and angles into a 2D array
    scan_points = np.round(scan_points, 3)  # Round each element in the array to 3 decimal places

    return scan_points


if __name__ == "__main__":
    # Continuously get LIDAR data and print it
    while True:
        lidarData = polarScan(54)  # Collect LIDAR data
        print(lidarData)  # Print the collected data
        time.sleep(1)  # Wait for 1 second before the next scan
