import RPi.GPIO as GPIO
import time
from lcd_display import *
from button_handler import *
from export import *

def main():
    # Main program block
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbers
    setup_buttons()
    lcd_init()

    production_start_time = None
    production_end_time = None
    production_active = False
    production_button_pressed = False

    pause_start_time = None
    pause_end_time = None
    pause_active = False
    pause_button_pressed = False

    panne_start_time = None
    panne_end_time = None
    panne_active = False
    panne_button_pressed = False

    changement_start_time = None
    changement_end_time = None
    changement_active = False
    changement_button_pressed = False

    reglage_start_time = None
    reglage_end_time = None
    reglage_active = False
    reglage_button_pressed = False

    organisation_start_time = None
    organisation_end_time = None
    organisation_active = False
    organisation_button_pressed = False

    # Initialize time variables
    elapsed_time_production = 0
    elapsed_time_pause = 0
    elapsed_time_panne = 0
    elapsed_time_reglage = 0
    elapsed_time_organisation = 0
    elapsed_time_changement = 0
    total_pause_time_during_panne = 0

    while True:
        # Display initial messages
        lcd_string("Labo ARRAZI", LCD_LINE_1)
        print("Labo ARRAZI")

        # Handle buttons
        # Check if pause button is pressed
        if GPIO.input(BUTTON_PAUSE_PIN) == GPIO.LOW and not pause_button_pressed:
            print("Pause button pressed")
            pause_button_pressed = True
            if not pause_active:
                pause_start_time = time.time()
                pause_active = True
            else:
                pause_end_time = time.time()
                pause_active = False
            time.sleep(1)  # 1-second pause after button click
        
        if GPIO.input(BUTTON_PAUSE_PIN) == GPIO.HIGH:
            pause_button_pressed = False

        # Check if panne button is pressed
        if GPIO.input(BUTTON_PANNE_PIN) == GPIO.LOW and not panne_button_pressed: 
            print("Panne button pressed")
            panne_button_pressed = True
            if not panne_active:
                panne_start_time = time.time()
                panne_active = True
                total_pause_time_during_panne = 0  # Reset total pause time during panne
            else:
                panne_end_time = time.time()
                panne_active = False
            time.sleep(1)  # 1-second pause after button click

        if GPIO.input(BUTTON_PANNE_PIN) == GPIO.HIGH:
            panne_button_pressed = False

        # Check if changement button is pressed
        if GPIO.input(BUTTON_CHANGEMENT_PIN) == GPIO.LOW and not changement_button_pressed:
            print("Changement button pressed")
            changement_button_pressed = True
            if not changement_active:
                changement_start_time = time.time()
                changement_active = True
            else:
                changement_end_time = time.time()
                changement_active = False
            time.sleep(1)  # 1-second pause after button click

        if GPIO.input(BUTTON_CHANGEMENT_PIN) == GPIO.HIGH:
            changement_button_pressed = False

        # Reglage button behavior
        if GPIO.input(BUTTON_REGLAGE_PIN) == GPIO.LOW and not reglage_button_pressed:
            print("Reglage button pressed")
            reglage_button_pressed = True
            if not reglage_active:
                reglage_start_time = time.time()
                reglage_active = True
            else:
                reglage_end_time = time.time()
                reglage_active = False
            time.sleep(1)  # 1-second pause after button click

        if GPIO.input(BUTTON_REGLAGE_PIN) == GPIO.HIGH:
            reglage_button_pressed = False

        # Organisation button behavior
        if GPIO.input(BUTTON_ORGANISATION_PIN) == GPIO.LOW and not organisation_button_pressed:
            print("Organisation button pressed")
            organisation_button_pressed = True
            if not organisation_active:
                organisation_start_time = time.time()
                organisation_active = True
            else:
                organisation_end_time = time.time()
                organisation_active = False
            time.sleep(1)  # 1-second pause after button click

        if GPIO.input(BUTTON_ORGANISATION_PIN) == GPIO.HIGH:
            organisation_button_pressed = False

        # Production button behavior
        if GPIO.input(BUTTON_PRODUCTION_PIN) == GPIO.LOW and not production_button_pressed:
            print("Production button pressed")
            production_button_pressed = True
            if not production_active:
                production_start_time = time.time()
                production_active = True
            else:
                production_end_time = time.time()
                production_active = False
                save_to_db(elapsed_time_production, elapsed_time_pause, elapsed_time_panne, elapsed_time_reglage, elapsed_time_organisation, elapsed_time_changement)
            time.sleep(1)  # 1-second pause after button click

        if GPIO.input(BUTTON_PRODUCTION_PIN) == GPIO.HIGH:
            production_button_pressed = False

        # Prepare display messages
        messages = ["Labo ARRAZI", "", "", ""]

        # Update production time
        if production_active:
            current_time = int(time.time() - production_start_time)
            minutes = current_time // 60
            seconds = current_time % 60
            messages[1] = f"Production: {minutes:02d}:{seconds:02d}"
        else:
            if production_end_time is not None:
                elapsed_time_production += int(production_end_time - production_start_time)
                production_end_time = None
            minutes = elapsed_time_production // 60
            seconds = elapsed_time_production % 60
            messages[1] = f"Total Production: {minutes:02d}:{seconds:02d}"

        # Update pause time
        if pause_active:
            current_time = int(time.time() - pause_start_time)
            minutes = current_time // 60
            seconds = current_time % 60
            messages[3] = f"Pause: {minutes:02d}:{seconds:02d}"
        else:
            if pause_end_time is not None:
                elapsed_time_pause += int(pause_end_time - pause_start_time)
                pause_end_time = None
            minutes = elapsed_time_pause // 60
            seconds = elapsed_time_pause % 60
            messages[3] = f"Total Pause: {minutes:02d}:{seconds:02d}"

        # Update panne time
        if panne_active:
            current_time = int(time.time() - panne_start_time - total_pause_time_during_panne)
            minutes = current_time // 60
            seconds = current_time % 60
            messages[2] = f"Panne: {minutes:02d}:{seconds:02d}"
        else:
            if panne_end_time is not None:
                elapsed_time_panne += int(panne_end_time - panne_start_time)
                panne_end_time = None
            minutes = elapsed_time_panne // 60
            seconds = elapsed_time_panne % 60
            messages[2] = f"Total Panne: {minutes:02d}:{seconds:02d}"

        # Display messages
        lcd_string(messages[0], LCD_LINE_1)
        lcd_string(messages[1], LCD_LINE_2)
        lcd_string(messages[2], LCD_LINE_3)
        lcd_string(messages[3], LCD_LINE_4)

        print(messages[0])
        print(messages[1])
        print(messages[2])
        print(messages[3])

        time.sleep(1)  # Pause after each button click

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        from lcd_display import lcd_byte, LCD_CMD, LCD_LINE_1
        lcd_byte(0x01, LCD_CMD)  # Clear the display
        lcd_string("Goodbye!", LCD_LINE_1)
        print("Goodbye!")
        time.sleep(2)  # Give enough time to display the goodbye message
        lcd_byte(0x01, LCD_CMD)  # Clear the display again
        GPIO.cleanup()