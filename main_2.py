import RPi.GPIO as GPIO
import time
from button_handler import *
from export import *

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
        'organisation': {'button_pin': BUTTON_ORGANISATION_PIN, 'active': False, 'button_pressed': False, 'start_time': None, 'end_time': None, 'elapsed_time': 0}
    }
    
    while True:
        print("Labo ARRAZI")
        is_machine_on = False
        vibration_detected = GPIO.input(16)
        detection_values.append(vibration_detected)
        start_time = time.time()
        if time.time() - start_time >= 1:
            print(str(mean_value))
            mean_value = sum(detection_values) / len(detection_values)
            print("Mean value detected: {:.5f}".format(mean_value))
            detection_values = []  # Reset the list
            start_time = time.time()  # Reset the timer
            if mean_value == 1.00000 :
                is_machine_on = False
                print("Machine is not on")
            else:
                is_machine_on = True
                print("Machine is on")
        
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
                    state['elapsed_time'] = 0

        if GPIO.input(states['production']['button_pin']) == GPIO.HIGH:
            states['production']['button_pressed'] = False

        if states['production']['active']:
            current_time = int(time.time() - states['production']['start_time'])
            minutes = current_time // 60
            seconds = current_time % 60
            print(f"Production: {minutes:02d}:{seconds:02d}")

        # Handle pause state separately
        if GPIO.input(states['pause']['button_pin']) == GPIO.LOW and not states['pause']['button_pressed']:
            states['pause']['button_pressed'] = True
            if not states['pause']['active']:
                states['pause']['start_time'] = time.time()
                states['pause']['active'] = True
            else:
                states['pause']['end_time'] = time.time()
                states['pause']['active'] = False
                elapsed_time = int(states['pause']['end_time'] - states['pause']['start_time'])
                states['pause']['elapsed_time'] += elapsed_time

                if states['reglage']['active']:
                    states['reglage']['elapsed_time'] -= elapsed_time

                if states['panne']['active']:
                    states['panne']['elapsed_time'] -= elapsed_time

        if GPIO.input(states['pause']['button_pin']) == GPIO.HIGH:
            states['pause']['button_pressed'] = False

        if states['pause']['active']:
            current_time = int(time.time() - states['pause']['start_time'])
            minutes = current_time // 60
            seconds = current_time % 60
            print(f"Pause: {minutes:02d}:{seconds:02d}")

        # Handle panne state separately
        if GPIO.input(states['panne']['button_pin']) == GPIO.LOW and not states['panne']['button_pressed']:
            states['panne']['button_pressed'] = True
            if not states['panne']['active']:
                states['panne']['start_time'] = time.time()
                states['panne']['active'] = True
            else:
                states['panne']['end_time'] = time.time()
                states['panne']['active'] = False
                elapsed_time = int(states['panne']['end_time'] - states['panne']['start_time'])
                states['panne']['elapsed_time'] += elapsed_time

        if GPIO.input(states['panne']['button_pin']) == GPIO.HIGH:
            states['panne']['button_pressed'] = False

        if states['panne']['active']:
            current_time = int(time.time() - states['panne']['start_time'])
            minutes = current_time // 60
            seconds = current_time % 60
            print(f"Panne: {minutes:02d}:{seconds:02d}")

        # Handle changement state separately
        if GPIO.input(states['changement']['button_pin']) == GPIO.LOW and not states['changement']['button_pressed']:
            states['changement']['button_pressed'] = True
            if not states['changement']['active']:
                states['changement']['start_time'] = time.time()
                states['changement']['active'] = True
            else:
                states['changement']['end_time'] = time.time()
                states['changement']['active'] = False
                elapsed_time = int(states['changement']['end_time'] - states['changement']['start_time'])
                states['changement']['elapsed_time'] += elapsed_time

        if GPIO.input(states['changement']['button_pin']) == GPIO.HIGH:
            states['changement']['button_pressed'] = False

        if states['changement']['active']:
            current_time = int(time.time() - states['changement']['start_time'])
            minutes = current_time // 60
            seconds = current_time % 60
            print(f"Changement: {minutes:02d}:{seconds:02d}")

        # Handle reglage state separately
        if GPIO.input(states['reglage']['button_pin']) == GPIO.LOW and not states['reglage']['button_pressed']:
            states['reglage']['button_pressed'] = True
            if not states['reglage']['active']:
                states['reglage']['start_time'] = time.time()
                states['reglage']['active'] = True
            else:
                states['reglage']['end_time'] = time.time()
                states['reglage']['active'] = False
                elapsed_time = int(states['reglage']['end_time'] - states['reglage']['start_time'])
                states['reglage']['elapsed_time'] += elapsed_time

        if GPIO.input(states['reglage']['button_pin']) == GPIO.HIGH:
            states['reglage']['button_pressed'] = False

        if states['reglage']['active']:
            current_time = int(time.time() - states['reglage']['start_time'])
            minutes = current_time // 60
            seconds = current_time % 60
            print(f"Reglage: {minutes:02d}:{seconds:02d}")

        # Handle organisation state separately
        if GPIO.input(states['organisation']['button_pin']) == GPIO.LOW and not states['organisation']['button_pressed']:
            states['organisation']['button_pressed'] = True
            if not states['organisation']['active']:
                states['organisation']['start_time'] = time.time()
                states['organisation']['active'] = True
            else:
                states['organisation']['end_time'] = time.time()
                states['organisation']['active'] = False
                elapsed_time = int(states['organisation']['end_time'] - states['organisation']['start_time'])
                states['organisation']['elapsed_time'] += elapsed_time

        if GPIO.input(states['organisation']['button_pin']) == GPIO.HIGH:
            states['organisation']['button_pressed'] = False

        if states['organisation']['active']:
            current_time = int(time.time() - states['organisation']['start_time'])
            minutes = current_time // 60
            seconds = current_time % 60
            print(f"Organisation: {minutes:02d}:{seconds:02d}")

        # Check if machine is on
        if not is_machine_on and not (states['panne']['active'] or states['pause']['active'] or states['organisation']['active'] or states['reglage']['active'] or states['changement']['active']):
            print("test")
        else:
            print("test")

        time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print("Goodbye!")
        GPIO.cleanup()
