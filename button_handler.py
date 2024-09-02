import RPi.GPIO as GPIO
import time

# Define GPIO for buttons
BUTTON_PAUSE_PIN = 27 # Button for "pause"
BUTTON_PANNE_PIN = 17  # Button for "panne"
BUTTON_CHANGEMENT_PIN =5   # Button for "changement"
BUTTON_PRODUCTION_PIN =22   # Button for "production"
BUTTON_REGLAGE_PIN = 13  # Button for "reglage"
BUTTON_ORGANISATION_PIN = 6  # Button for "organisation"
VIBRATION_PIN = 16

def setup_buttons():
    GPIO.setup(BUTTON_PRODUCTION_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button input for production
    GPIO.setup(BUTTON_PAUSE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button input for pause
    GPIO.setup(BUTTON_PANNE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button input for panne
    GPIO.setup(BUTTON_CHANGEMENT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button input for changement
    GPIO.setup(BUTTON_REGLAGE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button input for reglage
    GPIO.setup(BUTTON_ORGANISATION_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button input for organisation
    GPIO.setup(VIBRATION_PIN, GPIO.IN)  # Set GPIO16 as vibration input

