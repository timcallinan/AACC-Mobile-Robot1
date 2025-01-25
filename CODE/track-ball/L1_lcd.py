import time
import board
import adafruit_character_lcd.character_lcd_i2c as character_lcd

i2c = board.I2C()  # uses board.SCL and board.SDA
lcd = character_lcd.Character_LCD_I2C(i2c, columns=16, lines=2, address=0x21, backlight_inverted=False)

def lcdMessage(str):
#    print("lcdMessage:", str)
    lcd.message = str

if __name__ == "__main__":
    lcdMessage("This is a major test")
    
