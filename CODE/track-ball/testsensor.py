#!/usr/bin/env python
import time
from gpiozero import Button

sensorLeft = Button(5, pull_up=False)
sensorCenter = Button(6, pull_up=False)
sensorRight = Button(13, pull_up=False)

while True:
    left = int(sensorLeft.is_pressed)
    center = int(sensorCenter.is_pressed)
    right = int(sensorRight.is_pressed)
    #print(left, center, right)
    sensorKey = left*4 + center*2 + right
    print(left, center, right, "    ", sensorKey)
    time.sleep(1)

