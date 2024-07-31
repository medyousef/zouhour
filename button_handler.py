import RPi.GPIO as GPIO
import time

# Define GPIO for buttons
BUTTON_PAUSE_PIN = 17 # Button for "pause"
BUTTON_PANNE_PIN = 27  # Button for "panne"
BUTTON_CHANGEMENT_PIN = 22  # Button for "changement"
BUTTON_PRODUCTION_PIN = 5  # Button for "production"
BUTTON_REGLAGE_PIN = 6  # Button for "reglage"
BUTTON_ORGANISATION_PIN = 13  # Button for "organisation"

def setup_buttons():
    GPIO.setup(BUTTON_PRODUCTION_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button input for production
    GPIO.setup(BUTTON_PAUSE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button input for pause
    GPIO.setup(BUTTON_PANNE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button input for panne
    GPIO.setup(BUTTON_CHANGEMENT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button input for changement
    GPIO.setup(BUTTON_PRODUCTION_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button input for production
    GPIO.setup(BUTTON_REGLAGE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button input for reglage
    GPIO.setup(BUTTON_ORGANISATION_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button input for organisation

def handle_button(button_pin, button_pressed, active, start_time, end_time):
    if GPIO.input(button_pin) == GPIO.LOW and not button_pressed:
        button_pressed = True
        if not active:
            start_time = time.time()
            active = True
        else:
            end_time = time.time()
            active = False
        time.sleep(0.2)  # Debounce delay

    if GPIO.input(button_pin) == GPIO.HIGH:
        button_pressed = False

    return button_pressed, active, start_time, end_time
