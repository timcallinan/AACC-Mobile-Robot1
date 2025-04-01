Scuttle robot software for robot #1. (we need names for them)

As of 1/25/2025 the code integrates the gamepad for default control,
gamepad right trigger button enables line tracking and
gamepad left trigger button enables colored (orange) ball tracking using openCV.

3/31/2025
The directory 'lidar' contains the initial experiments with the RPLIDAR. Plots must be done
using connect.raspberrypi.com using screen sharing. (i.e. it won't work connecting via remote shell.)

plt.py - Test the matplotlib library for showing polar plots
lidar-test0.py - Simple test to retrieve a lidar scan.
lidar-test1.py - Based on lidar-test0.py, display the values from the scans.
display_lidar0.py - Initial test version of displaying the scans on a polar plot.
display_lidar1.py - Add radial limits to the polar plot to a radius of 5000 mm.
display_lidar2.py - Reverse angles on the plot so that it corresponds to right and left, looking down on the robot.

L1_lidar.py - Lidar script from Scuttle software repo, which was built for a different Lidar model.
L1_lidar1.py - Begin to make mods for the RPLidar unit.
