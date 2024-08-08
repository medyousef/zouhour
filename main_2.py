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

def update_times(state):
    if state['active']:
        current_time = get_elapsed_time(state['start_time'])
    else:
        if state['end_time'] is not None:
            state['elapsed_time'] += get_elapsed_time(state['start_time'], state['end_time'])
            state['end_time'] = None
        current_time = state['elapsed_time']
    
    minutes = current_time // 60
    seconds = current_time % 60
    return minutes, seconds

def handle_button(state, button_pin):
    if GPIO.input(button_pin) == GPIO.LOW and not state['button_pressed']:
        state['button_pressed'] = True
        if not state['active']:
            state['start_time'] = time.time()
            state['active'] = True
        else:
            state['end_time'] = time.time()
            state['active'] = False

    if GPIO.input(button_pin) == GPIO.HIGH:
        state['button_pressed'] = False
    
    minutes, seconds = update_times(state)
    return minutes, seconds

def main():
    initialize_gpio()
    
    states = {
        'production': {'button_pin': BUTTON_PRODUCTION_PIN, 'active': False, 'button_pressed': False, 'start_time': None, 'end_time': None, 'elapsed_time': 0},
        'pause': {'button_pin': BUTTON_PAUSE_PIN, 'active': False, 'button_pressed': False, 'start_time': None, 'end_time': None, 'elapsed_time': 0},
        'panne': {'button_pin': BUTTON_PANNE_PIN, 'active': False, 'button_pressed': False, 'start_time': None, 'end_time': None, 'elapsed_time': 0, 'total_pause_time_during_panne': 0},
        'changement': {'button_pin': BUTTON_CHANGEMENT_PIN, 'active': False, 'button_pressed': False, 'start_time': None, 'end_time': None, 'elapsed_time': 0},
        'reglage': {'button_pin': BUTTON_REGLAGE_PIN, 'active': False, 'button_pressed': False, 'start_time': None, 'end_time': None, 'elapsed_time': 0},
        'organisation': {'button_pin': BUTTON_ORGANISATION_PIN, 'active': False, 'button_pressed': False, 'start_time': None, 'end_time': None, 'elapsed_time': 0}
    }
    
    while True:
        print("Labo ARRAZI")
        
        for state_name, state in states.items():
            minutes, seconds = handle_button(state, state['button_pin'])
            if state_name == 'production':
                if state['active']:
                    print(f"Production: {minutes:02d}:{seconds:02d}")
                else:
                    print(f"Total Production: {minutes:02d}:{seconds:02d}")
                    save_to_db(state['elapsed_time'], states['pause']['elapsed_time'], states['panne']['elapsed_time'], states['reglage']['elapsed_time'], states['organisation']['elapsed_time'], states['changement']['elapsed_time'])
                    for state in states.values():
                        state['elapsed_time'] = 0
            else:
                print(f"{state_name.capitalize()}: {minutes:02d}:{seconds:02d}")
        time.sleep(1)
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print("Goodbye!")
        GPIO.cleanup()
