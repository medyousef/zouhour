import RPi.GPIO as GPIO
from lcd_display import lcd_byte, LCD_CMD, LCD_LINE_1, lcd_string
import time

def clean_lcd():
    # Clear the LCD display
    lcd_byte(0x01, LCD_CMD)  # Clear the display
    lcd_string("Goodbye!", LCD_LINE_1)
    time.sleep(2)  # Give enough time to display the goodbye message
    lcd_byte(0x01, LCD_CMD)  # Clear the display again
if __name__ == '__main__':
    clean_lcd()
    # Cleanup GPIO
    GPIO.cleanup()
    print("Cleaned")