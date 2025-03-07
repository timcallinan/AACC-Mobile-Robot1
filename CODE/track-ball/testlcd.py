#!/usr/bin/env python
# Test the 2x16 LCD panel at address 0x21
import time
import board
import adafruit_character_lcd.character_lcd_i2c as character_lcd

i2c = board.I2C()  # uses board.SCL and board.SDA
lcd = character_lcd.Character_LCD_I2C(i2c, columns=16, lines=2, address=0x21, backlight_inverted=False)

lcd.message = "Hello, world!"
time.sleep(2)

# Turn backlight on
lcd.backlight = True
# Print a two line message
lcd.message = "Hello\nCircuitPython"
# Wait 5s
time.sleep(5)
lcd.clear()
# Print two line message right to left
lcd.text_direction = lcd.RIGHT_TO_LEFT
lcd.message = "Hello\nCircuitPython"
# Wait 5s
time.sleep(5)
# Return text direction to left to right
lcd.text_direction = lcd.LEFT_TO_RIGHT
# Display cursor
lcd.clear()
lcd.cursor = True
lcd.message = "Cursor! "
# Wait 5s
time.sleep(5)
# Display blinking cursor
lcd.clear()
lcd.blink = True
lcd.message = "Blinky Cursor!"
# Wait 5s
time.sleep(5)
lcd.blink = False
lcd.clear()
# Create message to scroll
scroll_msg = "<-- Scroll"
lcd.message = scroll_msg
# Scroll message to the left
for i in range(len(scroll_msg)):
    time.sleep(0.5)
    lcd.move_left()
lcd.clear()
lcd.message = "Going to sleep\nCya later!"
time.sleep(3)
# Turn backlight off
lcd.backlight = False
time.sleep(2)
