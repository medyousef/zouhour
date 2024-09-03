import RPi.GPIO as GPIO
import time

# Define GPIO to LCD mapping
LCD_RS = 7
LCD_E  = 8
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18

# Define GPIO for buttons
BUTTON_PAUSE_PIN = 17
BUTTON_PANNE_PIN = 27  # New button for "panne"

# Define some device constants
LCD_WIDTH = 20    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

def main():
    # Main program block
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
    GPIO.setup(LCD_E, GPIO.OUT)  # E
    GPIO.setup(LCD_RS, GPIO.OUT) # RS
    GPIO.setup(LCD_D4, GPIO.OUT) # DB4
    GPIO.setup(LCD_D5, GPIO.OUT) # DB5
    GPIO.setup(LCD_D6, GPIO.OUT) # DB6
    GPIO.setup(LCD_D7, GPIO.OUT) # DB7
    GPIO.setup(BUTTON_PAUSE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button input for pause
    GPIO.setup(BUTTON_PANNE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button input for panne

    # Initialise display
    lcd_init()

    pause_start_time = None
    pause_end_time = None
    pause_active = False
    pause_button_pressed = False

    panne_start_time = None
    panne_end_time = None
    panne_active = False
    panne_button_pressed = False

    total_pause_time_during_panne = 0

    while True:
        # Display initial messages
        lcd_string("Labo ARRAZI", LCD_LINE_1)
        lcd_string("Machine BlistÃ©reuse", LCD_LINE_2)

        # Check if pause button is pressed
        if GPIO.input(BUTTON_PAUSE_PIN) == GPIO.LOW and not pause_button_pressed:
            pause_button_pressed = True
            if not pause_active:
                pause_start_time = time.time()
                pause_active = True
            else:
                pause_end_time = time.time()
                pause_active = False
                # Accumulate pause time if panne is active
                if panne_active:
                    total_pause_time_during_panne += pause_end_time - pause_start_time
            time.sleep(0.2)  # Debounce delay

        if GPIO.input(BUTTON_PAUSE_PIN) == GPIO.HIGH:
            pause_button_pressed = False

        # Check if panne button is pressed
        if GPIO.input(BUTTON_PANNE_PIN) == GPIO.LOW and not panne_button_pressed:
            panne_button_pressed = True
            if not panne_active:
                panne_start_time = time.time()
                panne_active = True
                total_pause_time_during_panne = 0  # Reset total pause time during panne
            else:
                panne_end_time = time.time()
                panne_active = False
            time.sleep(0.2)  # Debounce delay

        if GPIO.input(BUTTON_PANNE_PIN) == GPIO.HIGH:
            panne_button_pressed = False

        if pause_active:
            # Calculate the elapsed time
            elapsed_time = int(time.time() - pause_start_time)
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60
            # Update the LCD with the elapsed time in minutes and seconds
            lcd_string(f"Pause: {minutes:02d}:{seconds:02d}", LCD_LINE_3)
        else:
            if pause_end_time is not None:
                # Display the total pause time when not active
                elapsed_time = int(pause_end_time - pause_start_time)
                minutes = elapsed_time // 60
                seconds = elapsed_time % 60
                lcd_string(f"Total Pause: {minutes:02d}:{seconds:02d}", LCD_LINE_3)

        if panne_active:
            # Calculate the elapsed time
            elapsed_time = int(time.time() - panne_start_time - total_pause_time_during_panne)
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60
            # Update the LCD with the elapsed time in minutes and seconds
            lcd_string(f"Panne: {minutes:02d}:{seconds:02d}", LCD_LINE_4)
        else:
            if panne_end_time is not None:
                # Display the total panne time when not active
                elapsed_time = int(panne_end_time - panne_start_time - total_pause_time_during_panne)
                minutes = elapsed_time // 60
                seconds = elapsed_time % 60
                lcd_string(f"Total Panne: {minutes:02d}:{seconds:02d}", LCD_LINE_4)

        time.sleep(0.1)

def lcd_init():
    # Initialise display
    lcd_byte(0x33, LCD_CMD) # 110011 Initialise
    lcd_byte(0x32, LCD_CMD) # 110010 Initialise
    lcd_byte(0x06, LCD_CMD) # 000110 Cursor move direction
    lcd_byte(0x0C, LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
    lcd_byte(0x28, LCD_CMD) # 101000 Data length, number of lines, font size
    lcd_byte(0x01, LCD_CMD) # 000001 Clear display
    time.sleep(E_DELAY)

def lcd_byte(bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = True  for character
    #        False for command

    GPIO.output(LCD_RS, mode) # RS

    # High bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits&0x10==0x10:
        GPIO.output(LCD_D4, True)
    if bits&0x20==0x20:
        GPIO.output(LCD_D5, True)
    if bits&0x40==0x40:
        GPIO.output(LCD_D6, True)
    if bits&0x80==0x80:
        GPIO.output(LCD_D7, True)

    # Toggle 'Enable' pin
    lcd_toggle_enable()

    # Low bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits&0x01==0x01:
        GPIO.output(LCD_D4, True)
    if bits&0x02==0x02:
        GPIO.output(LCD_D5, True)
    if bits&0x04==0x04:
        GPIO.output(LCD_D6, True)
    if bits&0x08==0x08:
        GPIO.output(LCD_D7, True)

    # Toggle 'Enable' pin
    lcd_toggle_enable()

def lcd_toggle_enable():
    # Toggle enable
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)

def lcd_string(message, line):
    # Send string to display
    message = message.ljust(LCD_WIDTH, " ")

    lcd_byte(line, LCD_CMD)

    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd_byte(0x01, LCD_CMD)
        lcd_string("Goodbye!", LCD_LINE_1)
        GPIO.cleanup()