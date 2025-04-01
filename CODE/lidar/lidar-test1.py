# lidar-test1.py
# Modified RPLidar test scan version to show scan results
# It's possible to see the values change at a given angle
# as objects (like a hand) are moved into and out of the beam.
#
from rplidar import RPLidar
lidar = RPLidar('/dev/ttyUSB0')

info = lidar.get_info()
print(info)

health = lidar.get_health()
print(health)

for i, scan in enumerate(lidar.iter_scans()):
    print('%d: Got %d measurments' % (i, len(scan)))
    for j in scan:
#        if (j[1] > 0.0 and j[1] < 2.0):
        print(" ", j) 
#    if i > 2:
#        break

lidar.stop()
lidar.stop_motor()
lidar.disconnect()
