import RPi.GPIO as GPIO
import time
from button_handler import *
from export import *
from vibration import *

def initialize_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    setup_buttons()

def get_elapsed_time(start_time, end_time=None):
    if end_time:
        return int(end_time - start_time)
    else:
        return int(time.time() - start_time)

def main():
    initialize_gpio()
    detection_values = []
    start_time = time.time()

    states = {
        'production': {'button_pin': BUTTON_PRODUCTION_PIN, 'active': False, 'button_pressed': False, 'start_time': None, 'end_time': None, 'elapsed_time': 0},
        'pause': {'button_pin': BUTTON_PAUSE_PIN, 'active': False, 'button_pressed': False, 'start_time': None, 'end_time': None, 'elapsed_time': 0},
        'panne': {'button_pin': BUTTON_PANNE_PIN, 'active': False, 'button_pressed': False, 'start_time': None, 'end_time': None, 'elapsed_time': 0},
        'changement': {'button_pin': BUTTON_CHANGEMENT_PIN, 'active': False, 'button_pressed': False, 'start_time': None, 'end_time': None, 'elapsed_time': 0},
        'reglage': {'button_pin': BUTTON_REGLAGE_PIN, 'active': False, 'button_pressed': False, 'start_time': None, 'end_time': None, 'elapsed_time': 0},
        'organisation': {'button_pin': BUTTON_ORGANISATION_PIN, 'active': False, 'button_pressed': False, 'start_time': None, 'end_time': None, 'elapsed_time': 0},
        'is_machine_on': False,
        'signal_sonnore': 0
    }

    while True:
        print("Labo ARRAZI")

        # Check vibration and update is_machine_on
        is_machine_on, detection_values, start_time = check_vibration(detection_values, start_time)
        if is_machine_on is not None:
            states['is_machine_on'] = is_machine_on

        # Handle production state separately
        if GPIO.input(states['production']['button_pin']) == GPIO.LOW and not states['production']['button_pressed']:
            states['production']['button_pressed'] = True
            if not states['production']['active']:
                states['production']['start_time'] = time.time()
                states['production']['active'] = True
            else:
                states['production']['end_time'] = time.time()
                states['production']['active'] = False
                elapsed_time = int(states['production']['end_time'] - states['production']['start_time'])
                states['production']['elapsed_time'] += elapsed_time
                save_to_db(
                    states['production']['elapsed_time'],
                    states['pause']['elapsed_time'],
                    states['panne']['elapsed_time'],
                    states['reglage']['elapsed_time'],
                    states['organisation']['elapsed_time'],
                    states['changement']['elapsed_time']
                )
                # Reset all elapsed times to zero
                for state in states.values():
                    if isinstance(state, dict):  # Avoid resetting is_machine_on and signal_sonnore
                        state['elapsed_time'] = 0

        if GPIO.input(states['production']['button_pin']) == GPIO.HIGH:
            states['production']['button_pressed'] = False

        if states['production']['active']:
            current_time = int(time.time() - states['production']['start_time'])
            minutes = current_time // 60
            seconds = current_time % 60
            print(f"Production: {minutes:02d}:{seconds:02d}")

        # Handle other states (pause, panne, changement, reglage, organisation) similarly...

        # Check for signal_sonnore
        if not states['is_machine_on'] and not (states['panne']['active'] or states['pause']['active'] or states['organisation']['active'] or states['reglage']['active'] or states['changement']['active']):
            states['signal_sonnore'] = 1
        else:
            states['signal_sonnore'] = 0

        print(f"Signal Sonnore: {states['signal_sonnore']}")

        time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print("Goodbye!")
        GPIO.cleanup()